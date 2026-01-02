from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.models import User, UserRole
from app.core.security import get_password_hash

def reset_admin():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == "admin").first()
        if not user:
            print("Creating admin user...")
            user = User(
                username="admin",
                email="admin@example.com",
                full_name="Admin User",
                role=UserRole.ADMIN,
                is_active=True,
                password_hash=get_password_hash("admin123")
            )
            db.add(user)
        else:
            print("Updating admin password...")
            user.password_hash = get_password_hash("admin123")
            user.is_active = True
        
        db.commit()
        print("Admin user ready. Username: admin, Password: admin123")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_admin()
