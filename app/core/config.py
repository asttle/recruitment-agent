from pydantic import BaseSettings, PostgresDsn, validator
from typing import Optional, Dict, Any, List
import os
from pathlib import Path


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Recruitment Agent"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    
    # Database settings
    DATABASE_URL: Optional[PostgresDsn] = None
    
    # Email settings
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    
    # External API credentials
    LINKEDIN_API_KEY: Optional[str] = None
    LINKEDIN_API_SECRET: Optional[str] = None
    CVLIBRARY_API_KEY: Optional[str] = None
    NAUKRI_API_KEY: Optional[str] = None
    
    # LLM settings
    LLM_API_KEY: Optional[str] = None
    LLM_MODEL: str = "gpt-4"
    
    # File storage
    UPLOAD_DIR: Path = Path("./uploads")
    
    # JWT settings for authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development_secret_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
