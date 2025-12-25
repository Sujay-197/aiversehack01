import sys
import os

sys.path.append(os.getcwd())

from backend.agents.market_agent import MarketAgent

def test_real_search():
    print("--- Testing REAL Market Agent (Devpost + DDGS) ---")
    agent = MarketAgent()
    
    # Search for "AI" or "Python"
    query = "AI"
    print(f"Querying for: {query}")
    
    opps = agent.search(query)
    
    print("\n--- Results ---")
    if not opps:
        print("No opportunities found. (Check internet or selectors)")
    else:
        for i, opp in enumerate(opps):
            print(f"{i+1}. [{opp.type.upper()}] {opp.title}")
            print(f"   Source: {opp.source}")
            print(f"   URL: {opp.url}")
            print(f"   Reqs: {opp.requirements}")
            print("-" * 30)

if __name__ == "__main__":
    test_real_search()
