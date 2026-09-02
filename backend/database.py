import os
from pathlib import Path
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file in the backend directory
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL environment variable is not set. "
        "Please copy backend/.env.example to backend/.env and provide a valid connection string."
    )

# Create SQLAlchemy engine with connection pool pre-ping for cloud PostgreSQL (Neon)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

# Session factory for DB dependency injection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base for ORM Models
Base = declarative_base()

def get_db():
    """FastAPI dependency for managing database session lifecycle."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
