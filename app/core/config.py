import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Pimtong Work Manager"
    # Default: Try POSTGRES_URL (Vercel), then fallback to localhost
    # Note: If DATABASE_URL env var is set, pydantic will use it instead of this default.
    DATABASE_URL: str = os.getenv("POSTGRES_URL", "postgresql://user:password@localhost:5432/pimtong_db")
    
    # Fix for Vercel providing 'postgres://' which SQLAlchemy doesn't like (wants 'postgresql://')
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.DATABASE_URL.startswith("postgres://"):
             self.DATABASE_URL = self.DATABASE_URL.replace("postgres://", "postgresql://", 1)
    SECRET_KEY: str = "change_this_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = "YOUR_BOT_TOKEN_HERE"
    
    # AI
    GOOGLE_API_KEY: str = "YOUR_GOOGLE_API_KEY_HERE"

    class Config:
        env_file = ".env"

settings = Settings()
