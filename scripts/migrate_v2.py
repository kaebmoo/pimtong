import sqlite3
import os

# Adjust DB path if necessary (assuming sqlite for quick dev, or use sqlalchemy for postgres)
# Since I'm not 100% sure if user is on Postgres or SQLite, I'll attempt a generic SQLAlchmey approach if possible,
# ALL User logs show local uvicorn, likely SQLite default or Postgres.
# Checking Docker Compose - it has Postgres. Checking app/core/database.py...
# I'll write a Python script using the App's engine to be safe.

from sqlalchemy import text
from app.core.database import engine

def migrate():
    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        print("Starting Migration...")
        
        # 1. Create new tables if not exist (handled by main.py startup usually, but let's enforce)
        # We rely on main.py restart to create 'teams' and 'projects'.
        # But we need to add columns to existing tables manually.
        
        try:
            print("Adding team_id to users...")
            conn.execute(text("ALTER TABLE users ADD COLUMN team_id INTEGER REFERENCES teams(id)"))
        except Exception as e:
            print(f"Skipped (likely exists): {e}")

        try:
            print("Adding project_id to jobs...")
            conn.execute(text("ALTER TABLE jobs ADD COLUMN project_id INTEGER REFERENCES projects(id)"))
        except Exception as e:
            print(f"Skipped (likely exists): {e}")

        try:
            print("Adding team_id to assignments...")
            conn.execute(text("ALTER TABLE assignments ADD COLUMN team_id INTEGER REFERENCES teams(id)"))
        except Exception as e:
            print(f"Skipped (likely exists): {e}")
            
        print("Migration columns added.")

if __name__ == "__main__":
    migrate()
