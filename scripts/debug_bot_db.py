from app.core.database import SessionLocal
from app.models.models import User, Job, Assignment, Project
from sqlalchemy.orm import Session

def debug_db():
    db = SessionLocal()
    try:
        print("\n--- Users ---")
        users = db.query(User).all()
        for u in users:
            print(f"ID: {u.id}, User: {u.username}, Role: {u.role}, Telegram: {u.telegram_id}")

        print("\n--- Assignments ---")
        assignments = db.query(Assignment).all()
        for a in assignments:
            print(f"Job {a.job_id} -> Tech {a.technician_id}")

        print("\n--- Projects ---")
        projects = db.query(Project).all()
        for p in projects:
            print(f"ID: {p.id}, Name: {p.name}, Status: {p.status}")

        print("\n--- Jobs (Active) ---")
        jobs = db.query(Job).all()
        for j in jobs:
            print(f"ID: {j.id}, Title: {j.title}, Type: {j.job_type}, ProjectID: {j.project_id}")

    finally:
        db.close()

if __name__ == "__main__":
    debug_db()
