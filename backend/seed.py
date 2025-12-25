import uuid
import json
from datetime import datetime
from backend.models import ResumeEvidence, GitHubEvidence, LinkedInEvidence, Skill, GitHubRepo

# Mock Data Generation

def generate_mock_user_id() -> uuid.UUID:
    return uuid.uuid4()

def generate_mock_resume(user_id: uuid.UUID) -> ResumeEvidence:
    return ResumeEvidence(
        user_id=user_id,
        full_name="Alex Coder",
        email="alex@example.com",
        summary="Aspiring Full Stack Engineer with a passion for AI agents.",
        skills=[
            Skill(name="Python", category="Language", years_of_experience=2),
            Skill(name="React", category="Framework", years_of_experience=1.5),
            Skill(name="PostgreSQL", category="Database", years_of_experience=1),
        ],
        work_experience=[
            {
                "company": "TechStart Inc",
                "role": "Intern",
                "description": "Built internal tools using Python and Flask.",
                "start_date": "2023-06",
                "end_date": "2023-08"
            }
        ],
        education=[
            {
                "institution": "University of Tech",
                "degree": "B.S. Computer Science",
                "graduation_year": 2024
            }
        ]
    )

def generate_mock_github(user_id: uuid.UUID) -> GitHubEvidence:
    return GitHubEvidence(
        user_id=user_id,
        username="alexcoder123",
        bio="Building things with code.",
        public_repos=12,
        top_repositories=[
            GitHubRepo(name="portfolio-v1", url="https://github.com/alexcoder123/portfolio-v1", primary_language="JavaScript", stars=5),
            GitHubRepo(name="ai-chat-bot", url="https://github.com/alexcoder123/ai-chat-bot", primary_language="Python", stars=12, description="A simple chatbot using OpenAI API")
        ],
        followers=4
    )

def generate_mock_linkedin(user_id: uuid.UUID) -> LinkedInEvidence:
    return LinkedInEvidence(
        user_id=user_id,
        profile_url="https://linkedin.com/in/alexcoder",
        headline="CS Student | AI Enthusiast",
        about="I love building scalable systems and exploring new AI technologies.",
        skills=["Python", "JavaScript", "Communication", "Git"],
        experience=[
            {
                "company": "TechStart Inc",
                "title": "Software Engineering Intern",
                "duration": "3 months"
            }
        ]
    )

def seed_data():
    user_id = generate_mock_user_id()
    print(f"Generated User ID: {user_id}")
    
    resume = generate_mock_resume(user_id)
    github = generate_mock_github(user_id)
    linkedin = generate_mock_linkedin(user_id)
    
    print("\n--- Mock Resume ---")
    print(resume.model_dump_json(indent=2))
    
    print("\n--- Mock GitHub ---")
    print(github.model_dump_json(indent=2))

    print("\n--- Mock LinkedIn ---")
    print(linkedin.model_dump_json(indent=2))
    
    # In a real scenario, here we would connect to DB and insert.
    # For now, we print to stdout to verify Pydantic structure.
    # TODO: Connect to Postgres to insert these rows.

if __name__ == "__main__":
    seed_data()
