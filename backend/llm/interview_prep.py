"""
Interview Preparation Agent - Company-specific prep
"""
from typing import Dict, List
from backend.llm.client import LLMClient
from backend.models import Opportunity, BeliefState, GitHubEvidence

class InterviewPrepAgent:
    """
    Generates company and role-specific interview preparation
    """
    def __init__(self):
        self.llm = LLMClient()
    
    def prepare(
        self,
        opportunity: Opportunity,
        passport: BeliefState,
        github: GitHubEvidence = None
    ) -> Dict:
        """
        Generate interview prep for specific opportunity
        
        Args:
            opportunity: Target job
            passport: User's skills/experience
            github: Optional GitHub profile for concrete examples
            
        Returns:
            Dict with questions, suggested answers, and tips
        """
        # Build context
        user_skills_str = ", ".join([
            f"{attr} ({b.work_years:.0f}y)" 
            for attr, b in passport.beliefs.items() 
            if b.work_years > 0
        ])
        
        github_projects = ""
        if github:
            projects = [
                f"- {repo.name}: {repo.description} ({repo.primary_language}, {repo.stars} stars)"
                for repo in github.top_repositories[:3]
            ]
            github_projects = "\n".join(projects)
        
        prompt = f"""
You are an interview coach preparing a candidate.

Job Details:
- Title: {opportunity.title}
- Company: {opportunity.company}
- Requirements: {', '.join(opportunity.requirements)}

Candidate Profile:
- Skills: {user_skills_str}
- GitHub Projects:
{github_projects if github_projects else "None provided"}

Generate interview preparation:

1. **Likely Technical Questions** (3-5 questions they'll ask)
2. **Suggested Answers** (using candidate's actual experience)
3. **Questions to Ask** (3 smart questions for interviewer)
4. **Red Flags to Avoid** (common mistakes)

Return JSON:
{{
  "technical_questions": [
    {{
      "question": "How would you design a scalable API?",
      "suggested_answer": "Based on your microservices project...",
      "difficulty": "medium"
    }}
  ],
  "behavioral_questions": [
    {{
      "question": "Tell me about a time you debugged a complex issue",
      "suggested_answer": "Reference your GitHub commit where..."
    }}
  ],
  "questions_to_ask": [
    "What does success look like in this role?"
  ],
  "red_flags": [
    "Don't say 'I don't know' without offering to find out"
  ],
  "preparation_tips": [
    "Review your microservices architecture (likely to come up)"
  ]
}}
"""
        
        response = self.llm.generate(prompt, json_response=True)
        prep = self.llm.parse_json_response(response)
        
        # Add company research prompt
        prep["company_research"] = {
            "glassdoor": f"https://www.glassdoor.com/Search/results.htm?keyword={opportunity.company.replace(' ', '+')}",
            "linkedin": f"https://www.linkedin.com/company/{opportunity.company.replace(' ', '-').lower()}/",
            "news": f"https://news.google.com/search?q={opportunity.company.replace(' ', '+')}",
        }
        
        return prep
