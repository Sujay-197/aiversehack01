
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.dependencies import get_current_user
from backend import models_orm

router = APIRouter(prefix="/api/passport", tags=["passport"])

@router.get("/")
async def get_passport(
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Return mock belief state for MVP if DB is empty
    # In real version, we query models_orm.Belief associated with user.passport
    
    return {
        "beliefs": [
             { "skill": "Python (Backend)", "confidence": 0.72, "status": "verifying", "evidence": [{ "type": "github", "count": 12 }, { "type": "resume", "count": 1 }], "trend": 5 },
             { "skill": "React / Next.js", "confidence": 0.45, "status": "testing", "evidence": [{ "type": "github", "count": 3 }], "trend": -2 },
        ]
    }
