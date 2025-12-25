import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from backend.agents.market_agent import MarketAgent

def test_market_agent():
    print("--- Testing Market Agent (The Sensor) ---")
    
    agent = MarketAgent()
    opportunities = agent.search("Python")
    
    print(f"Found {len(opportunities)} opportunities.\n")
    
    for opp in opportunities:
        print(f"[{opp.type.upper()}] {opp.title} @ {opp.company}")
        print(f"   Requirements: {', '.join(opp.requirements)}")
        print(f"   URL: {opp.url}\n")
    
    # Assert
    assert len(opportunities) >= 3, "Should return at least 3 simulated opportunities"
    
    # Check for expected mock data
    has_python_role = any("Python" in o.requirements for o in opportunities)
    assert has_python_role, "Simulation should return a Python role"
    
    print("PASS: Market Agent returned valid test cases.")

if __name__ == "__main__":
    test_market_agent()
