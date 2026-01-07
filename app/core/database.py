from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

from sqlalchemy.pool import NullPool

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Use NullPool for serverless compatibility (Vercel) to prevent stale connections
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True, 
    poolclass=NullPool
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
