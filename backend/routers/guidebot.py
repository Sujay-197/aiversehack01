from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.dependencies import get_current_user
from backend import models_orm
from pydantic import BaseModel

router = APIRouter(prefix="/guidebot", tags=["guidebot"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_guidebot(
    req: ChatRequest,
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # In a real app, this would query the DB for the user's belief state
    # and use an LLM to generate a grounded response.
    # For now, we return a contextual mock.
    
    msg = req.message.lower()
    if "python" in msg:
        reply = "Looking at your GitHub, your Python confidence is around 72%. You've worked on 3 relevant projects, but none use advanced concurrency. I suggest a 'Testing Fit' experiment with a high-performance backend role."
    elif "series a" in msg or "startup" in msg:
        reply = "Startups value speed and direct evidence. Your 'React' expertise is well-documented, but your 'System Design' belief is still in the 'Learning' phase. Try building a small microservice ecosystem to boost that."
    else:
        reply = f"I've analyzed your career protocol. Your current path focus is {user.full_name or 'Researcher'}. To give better advice, could you run one more 'Calibration' experiment?"

    return ChatResponse(reply=reply)
