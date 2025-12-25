from textwrap import dedent
from google import genai

class tagExtracter:
  def __init__(self, api_key = None, model = ""):
    self.client = genai.Client(api_key=api_key)
    self.model = model

  def extract(resume_text):
      prompt = dedent(f"""
        You are an information extraction system.

        Extract structured information from the resume below.

        Rules:
        - Output valid JSON only
        - Normalize terms
        - Do not hallucinate missing data
        - If a field is not present, return null
        - No soft skills

        Output structure:
        {{
          "biodata": {{
            "full_name": string,
            "email": string,
            "phone": string,
            "location": string,
            "date_of_birth": string,
            "gender": string,
            "nationality": string
          }},
          "job_tags": {{
            "skills": [],
            "roles": [],
            "tools": [],
            "domains": [],
            "experience_level": string,
            "certifications": []
          }}
        }}

        Resume:
        \"\"\"{resume_text}\"\"\"
      """).strip()

      response = self.client.models.generate_content(
          model=self.model,
          contents=prompt
      )

      return response.text