from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend import models_orm
from backend.database import engine
from backend.routers import auth

# Create Tables (for local sqlite)
models_orm.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Aiversehack01 API")

# CORS Setup
origins = [
    "http://localhost:3000", # Next.js frontend
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to Aiversehack01 API"}
