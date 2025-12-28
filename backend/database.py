import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get Database URL from environment or use local SQLite as fallback
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/aiverse.db")
DATABASE_URL = "postgresql://postgres:1I2j3vacWAOjlFxF@db.bghirigkpwgysjtcesyd.supabase.co:5432/postgres"

# Supabase and some other providers might use 'postgres://' which SQLAlchemy 1.4+ deprecated
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Postgres requires different connection args (or rather, doesn't need the SQLite one)
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL, connect_args=connect_args
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
