import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Get Database URL from environment or use local SQLite as fallback
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if we should fallback to SQLite if no env var is set
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./backend/aiverse.db"

# Supabase and some other providers might use 'postgres://' which SQLAlchemy 1.4+ deprecated
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Render/Supabase connection args
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
else:
    # Important for Supabase pooler connections often needed on Render
    if "?" not in DATABASE_URL:
        DATABASE_URL += "?sslmode=require"

engine = create_engine(
    DATABASE_URL, 
    connect_args=connect_args,
    pool_pre_ping=True # Helps with connection resets on free tiers
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
