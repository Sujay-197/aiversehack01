import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from backend.seed import generate_mock_user_id, generate_mock_resume, generate_mock_github, generate_mock_linkedin
from backend.brain.passport import PassportGenerator
from backend.agents.market_agent import MarketAgent
from backend.brain.hypothesis import HypothesisGenerator

def test_hypothesis_engine():
    print("--- Testing Hypothesis Engine (The Scientist) ---")
    
    # 1. Setup State (Mock User + Passport)
    user_id = generate_mock_user_id()
    resume = generate_mock_resume(user_id)
    github = generate_mock_github(user_id)
    # Start with just Resume+GitHub to get the Python=0.9, React=0.3 setup
    
    passport_gen = PassportGenerator()
    passport = passport_gen.generate_initial_passport(user_id, resume, github)
    print(f"Passport Generated. Python Conf: {passport.beliefs['Python'].confidence}")
    
    # 2. Setup Market (Opportunities)
    market_agent = MarketAgent()
    opportunities = market_agent.search("Python") # Returns our 4 mock opps
    print(f"Market Scanned. Found {len(opportunities)} opportunities.\n")
    
    # 3. Generate Experiments
    hypo_gen = HypothesisGenerator()
    experiments = hypo_gen.generate_experiments(passport, opportunities)
    
    print(f"Generated {len(experiments)} Experiments:\n")
    
    for exp in experiments:
        # Find the opp title for display
        opp_title = next(o.title for o in opportunities if o.id == exp.opportunity_id)
        print(f"[{exp.type.upper()}] Apply to '{opp_title}'")
        print(f"   Hypothesis: {exp.hypothesis}")
        print(f"   Testing Belief: {exp.belief_id}\n")
        
    # Assertions
    # 1. expects "Python Backend Intern" -> Verification (High conf)
    python_exp = next((e for e in experiments if "Python Backend Intern" in next(o.title for o in opportunities if o.id == e.opportunity_id)), None)
    assert python_exp is not None, "Should propose applying to Python Intern"
    assert python_exp.type == "verification", "Python Intern should be a Verification experiment (High Conf)"
    
    # 2. expects "Frontend Developer" -> Learning (Partial match / low conf)
    frontend_exp = next((e for e in experiments if "Frontend Developer" in next(o.title for o in opportunities if o.id == e.opportunity_id)), None)
    if frontend_exp:
         # Depending on logic, might be learning or rejected logic. 
         # In our seed, React is 0.3 (Resume only). 
         # Requirements: React, JS, CSS. User has React(0.3), JS(0.4 from GitHub). Missing CSS.
         # Logic says: Partial Match -> Learning.
         assert frontend_exp.type == "learning", "Frontend should be Learning experiment"
         print("PASS: Frontend correctly identified as Learning opportunity.")

    # 3. Rust job -> Should be ignored (No skill match)
    rust_exp = next((e for e in experiments if "Systems Engineer" in next(o.title for o in opportunities if o.id == e.opportunity_id)), None)
    assert rust_exp is None, "Should NOT propose Rust job (No matching skills)"

    print("PASS: Hypothesis Engine logic verified.")

if __name__ == "__main__":
    test_hypothesis_engine()
