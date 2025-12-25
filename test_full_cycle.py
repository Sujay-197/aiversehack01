import sys
import os
import uuid

# Ensure project root is in path
sys.path.append(os.getcwd())

from backend.models import BeliefState, Belief, Experiment, Outcome, Opportunity
from backend.brain.reflection import Reflector
from backend.brain.graph import build_graph

def test_full_cycle():
    print("--- Testing Full Cycle (Plan -> Fail -> Learn -> Re-Plan) ---")
    
    # 1. Setup User and Graph
    user_id = uuid.uuid4()
    # High confidence initially
    initial_beliefs = {
        "Python": Belief(attribute="Python", confidence=0.9, basis="Self Assessment")
    }
    passport = BeliefState(user_id=user_id, beliefs=initial_beliefs)
    
    # Opportunity
    opp = Opportunity(
        title="Python Senior Dev",
        company="HardCorp",
        url="http://fail.com",
        type="job",
        requirements=["Python"]
    )
    
    app = build_graph()
    
    # 2. First Plan (Should be VERIFICATION)
    print("\n[Step 1] Initial Planning...")
    inputs = {"user_id": user_id, "opportunity": opp, "belief_state": passport, "relevant_beliefs": [], "proposed_experiment": None}
    res1 = app.invoke(inputs)
    exp1 = res1["proposed_experiment"]
    
    print(f"Plan 1: {exp1.type} | {exp1.hypothesis}")
    assert exp1.type == "verification", "Should be Verification initially"
    
    # 3. Simulate Failure (Rejection)
    print("\n[Step 2] Execution & Rejection...")
    outcome = Outcome(experiment_id=exp1.id, result="rejection", feedback="Failed technical interview")
    
    # 4. Reflect (Update Beliefs)
    print("[Step 3] Reflection...")
    reflector = Reflector()
    passport = reflector.reflect(passport, exp1, outcome)
    new_conf = passport.beliefs["Python"].confidence
    print(f"New Confidence: {new_conf}")
    
    # 5. Re-Plan (Identical Opportunity)
    # The graph should now see the history/lower confidence and propose something different or cautious.
    print("[Step 4] Re-Planning...")
    inputs["belief_state"] = passport # Update input with new state
    res2 = app.invoke(inputs)
    exp2 = res2["proposed_experiment"]
    
    print(f"Plan 2: {exp2.type} | {exp2.hypothesis}")
    
    # Assertions
    assert "CAUTION" in exp2.hypothesis or exp2.type == "learning", "New plan should be cautious"
    assert exp2.hypothesis != exp1.hypothesis, "Plan should change after failure"
    
    print("\nPASS: Full Cycle verified. The system adapted its strategy after failure.")

if __name__ == "__main__":
    test_full_cycle()
