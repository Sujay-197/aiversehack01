
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

def test_agents():
    print("Testing Agent Imports...")
    
    try:
        from backend.agents.resume_agent import ResumeAgent
        print("✅ ResumeAgent imported")
        assert ResumeAgent()
    except Exception as e:
        print(f"❌ ResumeAgent failed: {e}")

    try:
        from backend.agents.market_agent import MarketAgent
        print("✅ MarketAgent imported")
        assert MarketAgent()
    except Exception as e:
        print(f"❌ MarketAgent failed: {e}")

    try:
        from backend.agents.planner_agent import PlannerAgent
        print("✅ PlannerAgent imported")
        assert PlannerAgent()
    except Exception as e:
        print(f"❌ PlannerAgent failed: {e}")

    try:
        from backend.agents.reflection_agent import ReflectionAgent
        print("✅ ReflectionAgent imported")
        assert ReflectionAgent()
    except Exception as e:
        print(f"❌ ReflectionAgent failed: {e}")

    try:
        from backend.agents.action_agent import ActionAgent
        print("✅ ActionAgent imported")
        assert ActionAgent()
    except Exception as e:
        print(f"❌ ActionAgent failed: {e}")

if __name__ == "__main__":
    test_agents()
