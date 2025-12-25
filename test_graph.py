import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from backend.seed import generate_mock_user_id, generate_mock_resume, generate_mock_github
from backend.brain.passport import PassportGenerator
from backend.agents.market_agent import MarketAgent
from backend.brain.graph import build_graph

def test_graph_flow():
    print("--- Testing Semantic Reasoning Graph ---")
    
    # 1. Setup
    user_id = generate_mock_user_id()
    passport = PassportGenerator().generate_initial_passport(
        user_id, 
        generate_mock_resume(user_id), 
        generate_mock_github(user_id)
    )
    
    # 2. Get the "Python Backend Intern" opportunity (Reqs: Python, Flask, SQL)
    # Our user has Python(0.9), Postgres(0.3).
    # Missing logic: Postgres -> SQL.
    # The Vector Store should bridge "SQL" req -> "Postgres" belief.
    
    market = MarketAgent()
    opps = market.search("Python")
    target_opp = next(o for o in opps if "Intern" in o.title)
    
    print(f"Target: {target_opp.title}")
    print(f"Reqs: {target_opp.requirements}")
    print(f"User Beliefs: {list(passport.beliefs.keys())}")
    
    # 3. Run Graph
    app = build_graph()
    
    inputs = {
        "user_id": user_id,
        "opportunity": target_opp,
        "belief_state": passport,
        "relevant_beliefs": [],
        "proposed_experiment": None
    }
    
    print("\n--- Invoking Graph ---")
    result = app.invoke(inputs)
    
    # 4. Check Result
    exp = result["proposed_experiment"]
    print("\n--- Result ---")
    print(f"Experiment Type: {exp.type}")
    print(f"Hypothesis: {exp.hypothesis}")
    
    # Assertions
    # We expect "Python" (0.9) to trigger Verification.
    # We expect "SQL" requirement to find "PostgreSQL" belief via Semantic Search.
    
    assert exp.type == "verification", "Graph should conclude Verification"
    print("PASS: Graph executed successfully.")

if __name__ == "__main__":
    test_graph_flow()
