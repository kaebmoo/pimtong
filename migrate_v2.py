import sys
import os

# Create app context
sys.path.append(os.getcwd())

from app.core.database import engine
from sqlalchemy import text

def migrate():
    print("Migrating Database...")
    with engine.connect() as conn:
        # 1. Create JobHistory table
        print("Creating job_history table...")
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS job_history (
            id SERIAL PRIMARY KEY,
            job_id INTEGER,
            user_id INTEGER,
            old_status VARCHAR,
            new_status VARCHAR,
            note TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(job_id) REFERENCES jobs(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
        """))

        # SQLite workaround for adding columns if they don't exist
        # Check if columns exist first to avoid error
        columns = ["product_type", "model", "serial_number"]
        
        # This is a bit rough for SQLite but works for simple additions
        # Using a try-catch for adding columns is simpler than inspecting
        for col in columns:
            try:
                print(f"Adding column {col} to jobs...")
                conn.execute(text(f"ALTER TABLE jobs ADD COLUMN {col} VARCHAR;"))
            except Exception as e:
                print(f"Column {col} might already exist or error: {e}")
                
        conn.commit()
    print("Migration Complete.")

if __name__ == "__main__":
    migrate()
