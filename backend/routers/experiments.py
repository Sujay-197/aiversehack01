from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.dependencies import get_current_user
from backend import models_orm
from backend import models # Pydantic
from backend.agents.reflection_agent import ReflectionAgent
from backend.agents.action_agent import ActionAgent
import uuid
from typing import Optional

router = APIRouter(prefix="/api/experiments", tags=["experiments"])

try:
    reflection_agent = ReflectionAgent()
    action_agent = ActionAgent()
except Exception:
    reflection_agent = None
    action_agent = None

@router.get("/")
async def get_experiments(
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    experiments = db.query(models_orm.Experiment).filter(
        models_orm.Experiment.user_id == user.id
    ).order_by(models_orm.Experiment.created_at.desc()).all()
    
    results = []
    for exp in experiments:
        results.append({
            "id": exp.id,
            "role": exp.type,
            "title": exp.meta_data.get("role", exp.type) if exp.meta_data else exp.type,
            "company": exp.meta_data.get("company") if exp.meta_data else "",
            "hypothesis": exp.hypothesis,
            "status": exp.status,
            "confidence": 0.5, 
            "date": exp.created_at.strftime("%Y-%m-%d") if exp.created_at else "",
            "action_plan": exp.meta_data.get("action_plan") if exp.meta_data else []
        })
    return results

@router.post("/")
async def create_experiment(
    experiment_data: dict = Body(...),
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    User accepts a hypothesis -> Creates an Experiment
    Triggers ActionAgent to create a Plan.
    """
    # Create Pydantic model for Agent
    p_exp = models.Experiment(
        id=uuid.uuid4(),
        user_id=uuid.UUID(user.id),
        type=experiment_data.get("type", "learning"),
        hypothesis=experiment_data.get("statement", "Manual experiment"),
        belief_id=experiment_data.get("belief"),
        opportunity_id=uuid.uuid4(), # Mock
        meta_data={
            "role": experiment_data.get("role"),
            "company": experiment_data.get("company")
        }
    )

    # 1. Generate Action Plan
    action_plan = []
    if action_agent:
        action_plan = action_agent.generate_plan(p_exp)

    # 2. Save to DB
    new_exp = models_orm.Experiment(
        id=str(p_exp.id),
        user_id=user.id,
        type=p_exp.type,
        hypothesis=p_exp.hypothesis,
        status="active",
        meta_data={
            "role": experiment_data.get("role"),
            "company": experiment_data.get("company"),
            "belief_id": experiment_data.get("belief"),
            "action_plan": action_plan
        }
    )
    db.add(new_exp)
    db.commit()
    return {"status": "success", "id": new_exp.id, "action_plan": action_plan}

@router.post("/{experiment_id}/outcome")
async def report_outcome(
    experiment_id: str,
    outcome_data: dict = Body(...),
    user: models_orm.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    User reports result (Rejected, Offer, etc.) -> Trigger Reflection Agent
    """
    exp = db.query(models_orm.Experiment).filter(models_orm.Experiment.id == experiment_id, models_orm.Experiment.user_id == user.id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    # 1. Save Outcome
    outcome = models_orm.Outcome(
        experiment_id=exp.id,
        type=outcome_data.get("result", "unknown"),
        raw_response=outcome_data.get("feedback"),
        belief_impact={} 
    )
    db.add(outcome)
    
    # 2. Update Experiment Status
    exp.status = "completed" if outcome_data.get("result") in ["Rejected", "Offer", "Ghosted"] else "active"
    
    # 3. Trigger Reflection Agent
    if reflection_agent and reflection_agent.client:
        # Reconstruct Pydantic models needed for Agent
        p_exp = models.Experiment(
            id=uuid.UUID(exp.id),
            user_id=uuid.UUID(user.id),
            type=exp.type,
            hypothesis=exp.hypothesis,
            belief_id=exp.meta_data.get("belief_id") if exp.meta_data else None,
            opportunity_id=uuid.uuid4() # Mock needed
        )
        
        p_outcome = models.Outcome(
            experiment_id=uuid.UUID(exp.id),
            result=outcome.type,
            feedback=outcome.raw_response
        )
        
        # Fetch BeliefState
        orm_belief = user.belief_state
        if orm_belief:
             # Reconstruct BeliefState Pydantic
             current_beliefs = {}
             if "skills" in orm_belief.assumptions:
                 for skill in orm_belief.assumptions["skills"]:
                     current_beliefs[skill["name"]] = models.Belief(
                         attribute=skill["name"],
                         confidence=skill.get("confidence", 0.0),
                         basis=skill.get("source", "initial"),
                         context="Generated"
                     )
             
             p_state = models.BeliefState(
                 user_id=uuid.UUID(user.id),
                 beliefs=current_beliefs,
                 version=orm_belief.version or 1
             )
             
             # agent works
             updated_state = reflection_agent.reflect(p_state, p_exp, p_outcome)
             
             # Save back to DB
             new_assumptions = dict(orm_belief.assumptions)
             updated_skills = []
             for skill in new_assumptions.get("skills", []):
                 if skill["name"] in updated_state.beliefs:
                     skill["confidence"] = updated_state.beliefs[skill["name"]].confidence
                 updated_skills.append(skill)
             new_assumptions["skills"] = updated_skills
             
             orm_belief.assumptions = new_assumptions
             from sqlalchemy.orm.attributes import flag_modified
             flag_modified(orm_belief, "assumptions")

    db.commit()
    return {"status": "success", "message": "Outcome recorded and beliefs updated."}
