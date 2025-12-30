from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.dependencies import get_current_user
from backend import models_orm
from backend import models # Pydantic models
from backend.agents.planner_agent import PlannerAgent
from backend.agents.market_agent import MarketAgent
import uuid
from typing import List

router = APIRouter(prefix="/api/hypotheses", tags=["hypotheses"])

# Instantiate agents once (or dependency inject)
try:
    planner_agent = PlannerAgent()
    market_agent = MarketAgent()
except Exception:
    planner_agent = None
    market_agent = None

@router.get("/")
async def get_hypotheses(
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if agents are healthy
    if not planner_agent or not planner_agent.client:
        # Fallback to static if no LLM key
        return [
            { 
                "id": 1, 
                "statement": "LLM Key Missing: Cannot generate live hypotheses.",
                "risk": "Low",
                "belief": "Configuration",
                "reasoning": "Please set GEMINI_API_KEY in .env",
                "status": "warning" 
            }
        ]

    # 1. Fetch Belief State from DB
    orm_belief = db.query(models_orm.BeliefState).filter(models_orm.BeliefState.user_id == user.id, models_orm.BeliefState.is_active == True).first()
    
    if not orm_belief:
        return [] # No beliefs to plan against

    # Convert ORM to Pydantic for Agent
    # Note: `assumptions` column in DB is currently JSON, need to map it to BeliefState model structure
    # For MVP, we'll construct a pseudo-BeliefState or fix the model mapping later.
    # The Agent expects `BeliefState` pydantic model.
    
    # Quick fix: Construct a minimal BeliefState object
    current_beliefs = {}
    if "skills" in orm_belief.assumptions:
         for skill in orm_belief.assumptions["skills"]:
             current_beliefs[skill["name"]] = models.Belief(
                 attribute=skill["name"],
                 confidence=skill.get("confidence", 0.0),
                 basis=skill.get("source", "initial"),
                 context="Generated"
             )
    
    pydantic_belief_state = models.BeliefState(
        user_id=uuid.UUID(user.id),
        beliefs=current_beliefs,
        version=orm_belief.version or 1
    )

    # 2. Poll Market (Quick search based on top belief or generic "Software Engineer")
    # For optimization, we search for the top skill or a generic term
    search_query = "Software Engineer"
    if current_beliefs:
        # Search for the skill with lowest confidence (to learn) or highest (to verify)
        # Let's pick the first one for now
        search_query = list(current_beliefs.keys())[0]

    opportunities = market_agent.search(query=search_query)

    # 3. Plan
    experiments = planner_agent.generate_plan(pydantic_belief_state, opportunities, user.id)

    # 4. Filter and Format for Frontend
    # The frontend expects {id, statement, risk, belief, reasoning, status}
    results = []
    for exp in experiments:
        results.append({
            "id": str(exp.id),
            "statement": exp.hypothesis,
            "risk": "Medium" if exp.type == "verification" else "Low",
            "belief": exp.belief_id or "General",
            "reasoning": f"Testing {exp.type} opportunity at {exp.meta_data.get('company')}",
            "status": "active"
        })
        
        # Optional: Save these "proposed" experiments to DB?
        # For now, we generate them on the fly for the dashboard "Suggestions" view.
    
    return results
