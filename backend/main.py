import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import models_orm
from backend.database import engine
from backend.routers import auth

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create Tables on startup (only if not already there)
    # This prevents the app from hanging during import if DB is slow
    try:
        print("Connecting to database and creating tables...")
        models_orm.Base.metadata.create_all(bind=engine)
        print("Database tables verified.")
    except Exception as e:
        print(f"Database connection failed: {e}")
    yield

app = FastAPI(title="Aiversehack01 API", lifespan=lifespan)

# CORS Setup
origins = [
    "http://localhost:3000", # Next.js frontend
    "http://127.0.0.1:3000",
]

# Allow dynamic origins from environment (for Netlify/Production)
env_origins = os.getenv("ALLOWED_ORIGINS")
if env_origins:
    origins.extend([origin.strip() for origin in env_origins.split(",")])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
from backend.routers import onboarding, passport, hypotheses, experiments, insights, guidebot
app.include_router(onboarding.router)
app.include_router(passport.router)
app.include_router(hypotheses.router)
app.include_router(experiments.router)
app.include_router(insights.router)
app.include_router(guidebot.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Aiversehack01 API"}
