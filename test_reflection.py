import sys
import os
import uuid

# Ensure project root is in path
sys.path.append(os.getcwd())

from backend.models import BeliefState, Belief, Experiment, Outcome
from backend.brain.reflection import Reflector

def test_reflection_loop():
    print("--- Testing Reflection Loop (The Learning) ---")
    
    # 1. Setup User with Delusional Confidence
    user_id = uuid.uuid4()
    # User thinks they are a Python expert (0.9) but they maybe aren't.
    initial_beliefs = {
        "Python": Belief(attribute="Python", confidence=0.9, basis="Self Assessment")
    }
    state = BeliefState(user_id=user_id, beliefs=initial_beliefs)
    
    print(f"Initial Confidence in Python: {state.beliefs['Python'].confidence}")
    
    # 2. Creating a Verification Experiment that FAILED
    exp = Experiment(
        user_id=user_id,
        belief_id="Python",
        opportunity_id=uuid.uuid4(),
        type="verification",
        hypothesis="I am 0.9 confident, so I should get this.",
        status="completed"
    )
    
    # 3. Create the Outcome (Rejection)
    outcome = Outcome(
        experiment_id=exp.id,
        result="rejection",
        feedback="Failed coding assessment."
    )
    
    # 4. Run Reflection
    reflector = Reflector()
    updated_state = reflector.reflect(state, exp, outcome)
    
    # 5. Assertions
    new_conf = updated_state.beliefs["Python"].confidence
    print(f"Updated Confidence in Python: {new_conf}")
    
    # Should drop significantly because it was a "Verification" failure (Strong signal)
    # 0.9 - 0.15 = 0.75
    assert new_conf < 0.9, "Confidence should decrease after rejection"
    assert new_conf <= 0.8, "Should be a significant drop for verification failure"
    
    print("PASS: System learned from failure (Confidence Updated).")
    
    # Check History
    history = updated_state.beliefs["Python"].history
    print(f"History Log: {history[-1].reason}")

if __name__ == "__main__":
    test_reflection_loop()
