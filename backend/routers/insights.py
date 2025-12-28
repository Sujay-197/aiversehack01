
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.dependencies import get_current_user
from backend import models_orm

router = APIRouter(prefix="/api/insights", tags=["insights"])

@router.get("/")
async def get_insights(
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Retrieve user's insights
    return [
        {
            "id": 1,
            "date": "Oct 24",
            "trigger": "3 Rejections in Backend Roles",
            "delta": -8,
            "belief": "Python (Backend)",
            "insight": "Consistent failure in Senior roles suggests 'Senior' title is the mismatch, not the skill itself."
        }
    ]
