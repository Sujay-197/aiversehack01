import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get Database URL from environment or use local SQLite as fallback
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback to local SQLite if no DB URL is provided
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./backend/aiverse.db"

# Supabase Pooler Fixes:
# 1. Handle 'postgres://' -> 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 2. Ensure sslmode=require for cloud DBs if not already present
if "postgresql" in DATABASE_URL and "sslmode" not in DATABASE_URL:
    separator = "&" if "?" in DATABASE_URL else "?"
    DATABASE_URL += f"{separator}sslmode=require"

# Render/Supabase connection args
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True,  # Safety check for "Network unreachable" or "Connection reset"
    pool_recycle=300     # Refresh connections every 5 minutes
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
