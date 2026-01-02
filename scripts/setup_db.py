import sys
import os

# Add project root to python path
sys.path.append(os.getcwd())

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.core.database import Base
from app.models.models import User, UserRole

def init_db():
    # 1. Parse Database URL to get base connection info (users/pass) to creating the DB itself
    # Assuming DATABASE_URL format: postgresql://user:pass@host:port/dbname
    db_url = settings.DATABASE_URL
    if "postgresql" not in db_url:
        print("Error: Only PostgreSQL is supported for this script.")
        return

    # Extract db name
    base_url = db_url.rsplit('/', 1)[0]
    db_name = db_url.rsplit('/', 1)[1]
    
    # 2. Connect to default 'postgres' db to check/create target db
    print(f"Connecting to {base_url}/postgres to check DB '{db_name}'...")
    try:
        engine = create_engine(f"{base_url}/postgres", isolation_level="AUTOCOMMIT")
        with engine.connect() as conn:
            # Check if db exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            if not result.scalar():
                print(f"Database '{db_name}' does not exist. Creating...")
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"Database '{db_name}' created successfully.")
            else:
                print(f"Database '{db_name}' already exists.")
    except Exception as e:
        print(f"Error checking/creating database: {e}")
        print("Please ensure your PostgreSQL server is running and credentials in .env are correct.")
        return

    # 3. Connect to the actual DB to create tables
    print(f"Connecting to {db_url}...")
    engine = create_engine(db_url)
    Base.metadata.create_all(bind=engine)
    print("Tables created.")

    # 4. Create Admin User
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            print("Creating default admin user...")
            # Create Admin User
            from app.core.security import get_password_hash
            
            admin_user = User(
                username="admin",
                password_hash=get_password_hash("admin123"), 
                full_name="System Administrator",
                role=UserRole.ADMIN
            )
            db.add(admin_user)
            db.commit()
            print("Admin user created: username='admin', password='admin123'")
        else:
            print("Admin user already exists.")
    
    except Exception as e:
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
