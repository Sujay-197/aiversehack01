
import os
import PyPDF2
from google import genai
from textwrap import dedent
import json
import logging
from backend.config import config
from backend.models import ResumeEvidence, Skill

# Configure Logging
logger = logging.getLogger("ResumeAgent")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class ResumeAgent:
    def __init__(self):
        # Enforce usage of config or env vars via config
        # Note: config.py doesn't have API_KEY, so we still pull from env, but we log cleanly.
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not set. Resume analysis will fail.")
        
        self.client = genai.Client(api_key=api_key)
        self.model = config.LLM.MODEL_NAME

    def extract_text(self, pdf_path: str) -> str:
        """Extracts raw text from a PDF file."""
        if not os.path.exists(pdf_path):
            logger.error(f"PDF not found at {pdf_path}")
            raise FileNotFoundError(f"PDF not found at {pdf_path}")
            
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text()
            logger.info(f"Extracted {len(text)} characters from {pdf_path}")
            return text
        except Exception as e:
            logger.error(f"Failed to read PDF: {e}")
            raise

    def analyze(self, pdf_path: str, user_id=None) -> ResumeEvidence:
        """
        Extracts text from PDF and structured data using Gemini.
        Returns a populated ResumeEvidence object.
        """
        try:
            resume_text = self.extract_text(pdf_path)
            
            # Refined prompt with strict requirements
            prompt = dedent(f"""
            You are an expert HR AI. Extract structured data from this resume.
            
            OUTPUT INSTRUCTIONS:
            - Return ONLY valid JSON.
            - Do not include markdown formatting (```json ... ```).
            - Use `null` for missing fields.
            
            SCHEMA:
            {{
                "full_name": "string",
                "email": "string | null",
                "summary": "string | null",
                "skills": [
                    {{
                        "name": "string",
                        "category": "string (e.g. Language, Framework, Tool) | null",
                        "years_of_experience": "float | null"
                    }}
                ],
                "work_experience": [
                    {{
                        "company": "string",
                        "role": "string",
                        "start_date": "string",
                        "end_date": "string",
                        "description": "string"
                    }}
                ],
                "education": [
                    {{
                        "institution": "string",
                        "degree": "string",
                        "year": "string"
                    }}
                ]
            }}

            RESUME CONTENT:
            {resume_text}
            """).strip()

            logger.info(f"Sending resume to LLM ({self.model})...")
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            
            # Clean response if it still has markdown
            raw_text = response.text
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "").replace("```", "")
            
            data = json.loads(raw_text)
            logger.info("Successfully parsed JSON from LLM.")
            
            # Convert skills dicts to Skill objects
            skill_objs = [Skill(**s) for s in data.get("skills", [])]
            
            evidence = ResumeEvidence(
                user_id=user_id if user_id else "00000000-0000-0000-0000-000000000000",
                full_name=data.get("full_name", "Unknown"),
                email=data.get("email"),
                summary=data.get("summary"),
                skills=skill_objs,
                work_experience=data.get("work_experience", []),
                education=data.get("education", [])
            )
            return evidence

        except Exception as e:
            logger.error(f"Error analyzing resume: {e}")
            # Return empty/failed evidence
            return ResumeEvidence(
                user_id=user_id if user_id else "00000000-0000-0000-0000-000000000000",
                full_name="Parsing Failed",
                skills=[]
            )

if __name__ == "__main__":
    # Test stub
    agent = ResumeAgent()
    # print(agent.analyze("test.pdf"))
