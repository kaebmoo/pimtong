from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Pimtong Work Manager"
    # Default to standard docker-compose values, but prefer .env
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/pimtong_db"
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
