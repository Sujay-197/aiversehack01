from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.dependencies import get_current_user
from backend import models_orm
from pydantic import BaseModel
from backend.llm.client import LLMClient

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
    llm = LLMClient()
    user_name = user.full_name or "Researcher"

    # Fetch evidence from DB (query specific types directly to avoid SQLAlchemy boolean checks)
    resume_evidence = db.query(models_orm.Evidence).filter(models_orm.Evidence.user_id == user.id, models_orm.Evidence.type == 'resume').first()
    github_evidence = db.query(models_orm.Evidence).filter(models_orm.Evidence.user_id == user.id, models_orm.Evidence.type == 'github_repo').first()
    linkedin_evidence = db.query(models_orm.Evidence).filter(models_orm.Evidence.user_id == user.id, models_orm.Evidence.type == 'linkedin_profile').first()

    # Fetch belief state
    belief_state = db.query(models_orm.BeliefState).filter(models_orm.BeliefState.user_id == user.id, models_orm.BeliefState.is_active == True).first()

    # Fetch recent experiments
    experiments = db.query(models_orm.Experiment).filter(models_orm.Experiment.user_id == user.id).order_by(models_orm.Experiment.created_at.desc()).limit(3).all()

    # Format evidence for prompt
    resume_str = f"Resume: {resume_evidence.content_raw}" if resume_evidence else "Resume: Not found"
    github_str = f"GitHub: {github_evidence.content_raw}" if github_evidence else "GitHub: Not found"
    linkedin_str = f"LinkedIn: {linkedin_evidence.content_raw}" if linkedin_evidence else "LinkedIn: Not found"
    belief_str = f"Belief State: {belief_state.assumptions}" if belief_state else "Belief State: Not found"
    experiments_str = "\n".join([f"- {exp.type}: {exp.hypothesis} (status: {exp.status})" for exp in experiments]) or "No recent experiments."

    prompt = f"""
You are a career protocol guidebot for ambitious tech professionals. Your advice must be:
- Evidence-driven: Use the user's actual skills, GitHub projects, resume highlights, belief state, and experiment outcomes as evidence for your recommendations.
- Market-driven: Reference current job market trends, in-demand skills, and hiring signals for startups, Series A, and top tech companies.

User Evidence:
- Name: {user_name}
{resume_str}
{github_str}
{linkedin_str}
{belief_str}
Recent Experiments:
{experiments_str}

Instructions:
- When answering, cite specific evidence from the user's profile (e.g., "Your GitHub repo X shows...", "Your resume lists Y skill...").
- Suggest actions or experiments that are aligned with current market needs (e.g., "Given the demand for AI/ML, consider...", "Series A startups are hiring for...").
- If information is missing, ask a clarifying question to gather more evidence.
- Be concise, specific, and actionable.

Conversation:
User: {req.message}
Guidebot: (Respond with evidence-based, market-aware advice. Reference user's protocol and market context. If unsure, ask for more info.)
"""
    reply = llm.generate(prompt)
    return ChatResponse(reply=reply)
