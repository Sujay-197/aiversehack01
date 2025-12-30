
import logging
from typing import Dict, Any, List
from textwrap import dedent
import json
from google import genai
from backend.config import config
from backend.models import Experiment

# Configure Logging
logger = logging.getLogger("ActionAgent")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class ActionAgent:
    """
    The Lab Assistant.
    Executes the dirty work for experiments.
    """
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set. Action Agent will fail.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
        self.model = config.LLM.MODEL_NAME

    def generate_plan(self, experiment: Experiment) -> List[str]:
        """
        Generates a 3-5 step actionable checklist for the experiment.
        """
        prompt = dedent(f"""
        You are a Project Manager for a Career Lab. Create a 3-5 step tactical checklist to execute this experiment.
        
        Experiment:
        - Type: {experiment.type}
        - Hypothesis: {experiment.hypothesis}
        - Role/Topic: {experiment.meta_data.get('role', 'General')}
        
        OUTPUT INSTRUCTIONS:
        - Return ONLY a JSON list of strings.
        - Steps must be concrete actions (e.g. "Clone repo...", "Apply to X", "Watch tutorial on Y").
        - Keep it short (3-5 items max).
        
        Example: ["Find 3 job listings", "Tailor resume for keywords", "Submit applications"]
        """).strip()

        try:
            if not self.client:
                 return ["Define success criteria", "Execute experiment", "Report outcome"]

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            
            raw_text = response.text
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "").replace("```", "")
            
            steps = json.loads(raw_text)
            if isinstance(steps, list):
                return steps
            return ["Execute experiment"]

        except Exception as e:
            logger.error(f"Action plan generation failed: {e}")
            return ["Start experiment", "Complete required tasks", "Report outcome"]
