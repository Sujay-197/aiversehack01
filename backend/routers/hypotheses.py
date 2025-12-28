
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.dependencies import get_current_user
from backend import models_orm

router = APIRouter(prefix="/api/hypotheses", tags=["hypotheses"])

@router.get("/")
async def get_hypotheses(
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Determine hypotheses based on belief state GAP analysis
    # For MVP, returning the static list but as a JSON response
    return [
        { 
            "id": 1, 
            "statement": "Applying to 5 Senior Backend roles will cause rejections, validating that I am currently Mid-Level.",
            "risk": "Low",
            "belief": "Python (Backend)",
            "reasoning": "Confidence 0.72 is high but unverified in market.",
            "status": "active" 
        },
        { 
            "id": 2, 
            "statement": "Contributing to a Fintech Open Source repo will boost System Design confidence by 10%.",
            "risk": "Medium",
            "belief": "System Design",
            "reasoning": "Current confidence 0.25 is too low for applications.",
            "status": "proposed" 
        }
    ]
