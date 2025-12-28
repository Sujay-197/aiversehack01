
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.dependencies import get_current_user
from backend import models_orm

router = APIRouter(prefix="/api/experiments", tags=["experiments"])

@router.get("/")
async def get_experiments(
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Retrieve user's experiments
    # For MVP, return mock
    return [
        {
            "id": 1,
            "role": "Senior Backend Engineer",
            "company": "Vercel",
            "status": "Ghosted",
            "date": "2 weeks ago",
            "hypothesis_id": 1
        },
        {
            "id": 2,
            "role": "Software Engineer Intern",
            "company": "Google",
            "status": "Rejected",
            "date": "3 days ago",
            "hypothesis_id": 1
        }
    ]
