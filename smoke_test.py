
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing Agent Imports...")
    from backend.agents.resume_agent import ResumeAgent
    from backend.agents.github_agent import GitHubAgent
    from backend.agents.market_agent import MarketAgent
    print("Imports Successful.")

    print("Testing Agent Instantiation...")
    resume = ResumeAgent()
    print("ResumeAgent Initialized.")
    
    github = GitHubAgent()
    print("GitHubAgent Initialized.")
    
    market = MarketAgent()
    print("MarketAgent Initialized.")
    
    print("SMOKE TEST PASSED.")
except Exception as e:
    print(f"SMOKE TEST FAILED: {e}")
    sys.exit(1)
