"""
Resume Parser - LLM-powered resume data extraction
"""
from typing import Dict, List
from backend.llm.client import LLMClient
from backend.models import ResumeEvidence, Skill
import uuid

class ResumeParser:
    """
    Extracts structured data from resume text using LLM
    """
    def __init__(self):
        self.llm = LLMClient()
    
    def parse(self, resume_text: str, user_id: uuid.UUID = None) -> ResumeEvidence:
        """
        Parse resume text into structured ResumeEvidence
        
        Args:
            resume_text: Raw resume text (from PDF/DOCX)
            user_id: Optional user ID
            
        Returns:
            ResumeEvidence object
        """
        if user_id is None:
            user_id = uuid.uuid4()
        
        prompt = f"""
You are a resume parser. Extract structured data from this resume.

Resume:
{resume_text}

Return ONLY valid JSON (no markdown, no explanation):
{{
  "full_name": "string",
  "email": "string or null",
  "summary": "brief 1-sentence profile summary",
  "skills": [
    {{
      "name": "Python",
      "category": "Language",
      "years_of_experience": 3.0
    }}
  ],
  "work_experience": [
    {{
      "title": "Software Engineer",
      "company": "TechCorp",
      "years": 2.5,
      "description": "brief summary"
    }}
  ],
  "education": [
    {{
      "degree": "BS Computer Science",
      "institution": "University",
      "year": 2020
    }}
  ]
}}

Rules:
- Extract ALL skills mentioned (languages, frameworks, tools)
- Infer years_of_experience from job duration or context
- If years unclear, estimate conservatively
- Return valid JSON only
"""
        
        response = self.llm.generate(prompt, json_response=True)
        data = self.llm.parse_json_response(response)
        
        # Convert to Pydantic models
        skills = [
            Skill(
                name=s["name"],
                category=s.get("category", "Technical"),
                years_of_experience=s.get("years_of_experience", 0.0)
            )
            for s in data.get("skills", [])
        ]
        
        return ResumeEvidence(
            user_id=user_id,
            full_name=data.get("full_name", "Unknown"),
            email=data.get("email"),
            summary=data.get("summary"),
            skills=skills,
            work_experience=data.get("work_experience", []),
            education=data.get("education", [])
        )
