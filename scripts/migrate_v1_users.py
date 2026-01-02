import sys
import os

# Add project root to python path
sys.path.append(os.getcwd())

from sqlalchemy import create_engine, text
from app.core.config import settings

def migrate():
    print(f"Connecting to database...")
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        
        # Add phone_number
        try:
            print("Adding column 'phone_number'...")
            conn.execute(text("ALTER TABLE users ADD COLUMN phone_number VARCHAR"))
            print("Column 'phone_number' added.")
        except Exception as e:
            print(f"Skipping phone_number (maybe exists): {e}")

        # Add email
        try:
            print("Adding column 'email'...")
            conn.execute(text("ALTER TABLE users ADD COLUMN email VARCHAR"))
            print("Column 'email' added.")
        except Exception as e:
            print(f"Skipping email (maybe exists): {e}")

if __name__ == "__main__":
    migrate()
