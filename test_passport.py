import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from backend.seed import generate_mock_user_id, generate_mock_resume, generate_mock_github, generate_mock_linkedin
from backend.brain.passport import PassportGenerator

def test_passport_generation():
    print("--- Starting Passport Generation Test ---")
    
    # 1. Generate Mock Data
    user_id = generate_mock_user_id()
    resume = generate_mock_resume(user_id)
    github = generate_mock_github(user_id)
    linkedin = generate_mock_linkedin(user_id)
    print(f"Mock Data Ready for User: {user_id}")

    # 2. Instantiate Generator
    generator = PassportGenerator()
    
    # 3. Generate Passport
    print("Synthesizing Beliefs...")
    passport = generator.generate_initial_passport(user_id, resume, github, linkedin)
    
    # 4. Verify Output
    print("\n--- Failure Passport (Belief State) ---")
    print(passport.model_dump_json(indent=2))
    
    # Assertions
    beliefs = passport.beliefs
    
    # Check "Python" - Should be in Resume (0.3) + GitHub (0.4) + Star Bonus (0.1) = ~0.8
    # Actually logic: 
    # Resume: += 0.3
    # GitHub (ai-chat-bot): += 0.4 + 0.1 (12 stars > 5) = 0.5
    # Total ~0.8
    
    python_conf = beliefs.get("Python").confidence
    print(f"\nVerifying 'Python' Confidence: {python_conf}")
    
    if python_conf >= 0.7:
        print("PASS: Python confidence is high as expected (Resume + GitHub).")
    else:
        print(f"FAIL: Python confidence {python_conf} is lower than expected.")

    # Check "React" - Only in Resume (0.3)
    react_conf = beliefs.get("React").confidence
    print(f"Verifying 'React' Confidence: {react_conf}")
    
    if 0.25 <= react_conf <= 0.35:
        print("PASS: React confidence is around 0.3 (Resume only).")
    else:
        print("WARNING: React confidence unexpectedly high/low.")

if __name__ == "__main__":
    test_passport_generation()
