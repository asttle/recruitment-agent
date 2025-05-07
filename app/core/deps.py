from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Create SQLAlchemy engine
if settings.DATABASE_URL:
    engine = create_engine(settings.DATABASE_URL)
else:
    # Default to SQLite for development if no DB URL provided
    SQLALCHEMY_DATABASE_URL = "sqlite:///./recruitment_agent.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Dependency for getting DB session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 