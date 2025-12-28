
from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.dependencies import get_current_user
from backend import models_orm
from typing import Optional
import shutil
import os

router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])

@router.post("/ingest")
async def ingest_evidence(
    file: Optional[UploadFile] = File(None),
    github_url: Optional[str] = Form(None),
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Save File if exists
    if file:
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        file_path = f"{upload_dir}/{user.id}_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Trigger parsing agent (Future)
        print(f"File saved to {file_path}")

    # 2. Save GitHub URL
    if github_url:
        # Trigger GitHub parsing agent (Future)
        print(f"GitHub URL received: {github_url}")

    # 3. Create initial 'Passport' data (Mocking the 'Agent' work)
    # Check if passport exists
    if not user.belief_state:
        # Create initial empty state
        initial_state = {
            "beliefs": [],
            "status": "initialized"
        }
        passport = models_orm.BeliefState(user_id=user.id, assumptions=initial_state)
        db.add(passport)
        db.commit()
        
    return {"status": "success", "message": "Evidence received. Agents dispatched."}

@router.post("/clarify")
async def save_preferences(
    preferences: dict,
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Save preferences to user profile or context
    # user.preferences = preferences # If column existed
    return {"status": "success", "message": "Preferences saved."}
