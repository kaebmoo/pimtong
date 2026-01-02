import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.api.api import api_router
from app.core.database import engine, Base, SessionLocal
from app.core.security import get_password_hash
from app.models.models import User, UserRole

app = FastAPI(title=settings.PROJECT_NAME)

# Ensure static directory exists
static_dir = "app/static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(api_router, prefix="/api")

@app.get("/setup/seed")
async def seed_db():
    """Manual trigger to seed database for Vercel"""
    try:
        # Create Tables
        Base.metadata.create_all(bind=engine)
        
        # Init Admin
        db = SessionLocal()
        try:
            if not db.query(User).first():
                admin_user = User(
                    username="admin",
                    password_hash=get_password_hash("admin"),
                    full_name="System Administrator",
                    role=UserRole.ADMIN,
                    phone_number="000-000-0000",
                    is_active=True
                )
                db.add(admin_user)
                db.commit()
                return {"message": "Admin user created successfully. Use: admin / admin", "status": "seeded"}
            else:
                return {"message": "Database already initialized (users exist).", "status": "skipped"}
        finally:
            db.close()
    except Exception as e:
        return {"error": str(e), "status": "failed"}

@app.on_event("startup")
def startup_event():
    # Create tables
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating tables: {e}")
    
    # Init Admin
    try:
        db = SessionLocal()
        try:
            # Check if user table exists and has users
            # Note: query(User) might fail if table doesn't exist yet if create_all failed (e.g. conn error)
            # But we catch that outside.
            if not db.query(User).first():
                print("--- NO USERS FOUND: Seeding Default Admin ---")
                admin_user = User(
                    username="admin",
                    password_hash=get_password_hash("admin"),
                    full_name="System Administrator",
                    role=UserRole.ADMIN,
                    phone_number="000-000-0000",
                    is_active=True
                )
                db.add(admin_user)
                db.commit()
                print("--- DEFAULT ADMIN CREATED: admin / admin ---")
        finally:
            db.close()
    except Exception as e:
        print(f"Startup seeding failed: {e}")

# Web routes will be added separately or here
from fastapi import Request, Depends
from fastapi.responses import HTMLResponse

from app.api.deps import get_current_user_from_cookie
from fastapi.responses import RedirectResponse
from app.models.models import User
from typing import Optional

templates = Jinja2Templates(directory="app/templates")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
async def read_root(
    request: Request, 
    user: Optional[User] = Depends(get_current_user_from_cookie)
):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})

@app.get("/team", response_class=HTMLResponse)
async def read_team(
    request: Request,
    user: Optional[User] = Depends(get_current_user_from_cookie)
):
    if not user:
         return RedirectResponse(url="/login")
    if user.role != "admin" and user.role != "manager":
         # Simple RBAC: View Only or Restricted? 
         # For now allow view but maybe hide controls in template
         pass
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

@app.get("/jobs", response_class=HTMLResponse)
async def read_jobs_page(
    request: Request,
    user: Optional[User] = Depends(get_current_user_from_cookie)
):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("jobs.html", {"request": request, "user": user})

@app.get("/calendar", response_class=HTMLResponse)
async def read_calendar_page(
    request: Request,
    user: Optional[User] = Depends(get_current_user_from_cookie)
):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("calendar.html", {"request": request, "user": user})

@app.get("/performance", response_class=HTMLResponse)
async def read_performance_page(
    request: Request,
    user: Optional[User] = Depends(get_current_user_from_cookie)
):
    if not user:
        return RedirectResponse(url="/login")
    if user.role not in ["admin", "manager"]:
        # Maybe technicians shouldn't see full business performance
        pass 
    return templates.TemplateResponse("performance.html", {"request": request, "user": user})

@app.get("/profile", response_class=HTMLResponse)
async def read_profile_page(
    request: Request,
    user: Optional[User] = Depends(get_current_user_from_cookie)
):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

@app.get("/teams", response_class=HTMLResponse)
async def read_teams_page(
    request: Request,
    user: Optional[User] = Depends(get_current_user_from_cookie)
):
    if not user:
        return RedirectResponse(url="/login")
    if user.role not in ["admin", "staff"]:
        # Standard users shouldn't manage teams
         return RedirectResponse(url="/")
    return templates.TemplateResponse("teams.html", {"request": request, "user": user})

@app.get("/projects", response_class=HTMLResponse)
async def read_projects_page(
    request: Request,
    user: Optional[User] = Depends(get_current_user_from_cookie)
):
    if not user:
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("projects.html", {"request": request, "user": user})

@app.get("/reports", response_class=HTMLResponse)
async def read_reports_page(
    request: Request,
    user: Optional[User] = Depends(get_current_user_from_cookie)
):
    if not user:
        return RedirectResponse(url="/login")
    if user.role not in ["admin", "staff"]:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("reports.html", {"request": request, "user": user})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=9000, reload=True)
