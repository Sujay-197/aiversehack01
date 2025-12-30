from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.dependencies import get_current_user
from backend import models_orm
from typing import Optional
import shutil
import os
import json

router = APIRouter(prefix="/api/onboarding", tags=["onboarding"])

@router.get("/status")
async def check_status(
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if user has any evidence (Resume or GitHub)
    has_resume = db.query(models_orm.Evidence).filter(
        models_orm.Evidence.user_id == user.id,
        models_orm.Evidence.type == 'resume'
    ).first() is not None
    
    has_github = db.query(models_orm.Evidence).filter(
        models_orm.Evidence.user_id == user.id,
        models_orm.Evidence.type == 'github_repo'
    ).first() is not None

    return {
        "is_onboarded": has_resume or has_github,
        "details": {"resume": has_resume, "github": has_github}
    }

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
        
        # Create Evidence record for Resume
        # Check if exists to update or create
        resume_evidence = db.query(models_orm.Evidence).filter(
            models_orm.Evidence.user_id == user.id, 
            models_orm.Evidence.type == 'resume'
        ).first()

        if not resume_evidence:
            resume_evidence = models_orm.Evidence(
                user_id=user.id,
                type='resume',
                content_raw={"file_path": file_path, "filename": file.filename},
                source_url=file_path
            )
            db.add(resume_evidence)
        else:
            resume_evidence.content_raw = {"file_path": file_path, "filename": file.filename}
    
    # 2. Save GitHub URL
    if github_url:
        # Create Evidence record for GitHub
        github_evidence = db.query(models_orm.Evidence).filter(
            models_orm.Evidence.user_id == user.id, 
            models_orm.Evidence.type == 'github_repo'
        ).first()

        if not github_evidence:
            github_evidence = models_orm.Evidence(
                user_id=user.id,
                type='github_repo',
                content_raw={"url": github_url},
                source_url=github_url
            )
            db.add(github_evidence)
        else:
            github_evidence.content_raw = {"url": github_url}

    # 3. Create initial 'Passport' data (Mocking the 'Agent' work)
    # Check if passport exists
    if not user.belief_state:
        # Create initial empty state with some default beliefs to verify flow
        initial_state = {
            "execution_status": "initialized",
            "skills": [
                {"name": "Python", "confidence": 0.5, "source": "inferred_initial"},
                {"name": "General Engineering", "confidence": 0.3, "source": "inferred_initial"}
            ]
        }
        passport = models_orm.BeliefState(user_id=user.id, assumptions=initial_state)
        db.add(passport)
    
    db.commit()
        
    return {"status": "success", "message": "Evidence received and stored."}

@router.post("/clarify")
async def save_preferences(
    preferences: dict,
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Save preferences to belief state metadata or user profile
    # For now, update the BeliefState if it exists
    if user.belief_state:
        current_assumptions = dict(user.belief_state.assumptions)
        current_assumptions["preferences"] = preferences
        user.belief_state.assumptions = current_assumptions
        # Force update flag for SQLAlchemy to detect JSON change
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(user.belief_state, "assumptions")
        
        db.commit()

    return {"status": "success", "message": "Preferences saved."}
