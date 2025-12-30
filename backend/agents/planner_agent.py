
import logging
from typing import List
from textwrap import dedent
import json
from google import genai
from backend.config import config
from backend.models import BeliefState, Experiment, Opportunity

# Configure Logging
logger = logging.getLogger("PlannerAgent")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class PlannerAgent:
    """
    The Career Strategist.
    analyzes BeliefState + Market Opportunities -> Generates Experiments.
    """
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set. Planner will fail.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
        self.model = config.LLM.MODEL_NAME

    def generate_plan(self, belief_state: BeliefState, opportunities: List[Opportunity], user_id: str) -> List[Experiment]:
        """
        Generates a list of Experiments based on the current Belief State and Market Opportunities.
        """
        # Convert inputs to string for prompt
        beliefs_str = json.dumps(belief_state.model_dump(include={'beliefs'}), default=str, indent=2)
        opps_str = json.dumps([opp.model_dump() for opp in opportunities], default=str, indent=2)

        prompt = dedent(f"""
        You are a Career Scientist. Design experiments to test the user's career readiness.

        INPUT DATA:
        1. Belief State (User's presumed skills & confidence):
        {beliefs_str}

        2. Market Opportunities (Potential experiments):
        {opps_str}

        TASK:
        Select the best opportunities to test the user's beliefs. 
        - If confidence is LOW (<0.4), suggest "Learning" experiments (e.g. Hackathons, Projects).
        - If confidence is MEDIUM/HIGH (>0.6), suggest "Verification" experiments (e.g. Jobs, Internships).
        - Create a specific HYPOTHESIS for each experiment.

        OUTPUT JSON LIST (No Markdown):
        [
            {{
                "type": "verification" | "learning",
                "hypothesis": "If I apply to X, I will confirm my Y skill because...",
                "opportunity_id": "uuid_of_opportunity",
                "belief_target": "Skill Name"
            }}
        ]
        """).strip()

        try:
            logger.info("Generating experiment plan...")
            response = self.client.models.generate_content(
                model=self.model, 
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            
            raw_text = response.text
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "").replace("```", "")
            
            plan_data = json.loads(raw_text)
            
            experiments = []
            for item in plan_data:
                # Find matching opportunity to get full data if needed, or just link by ID
                # For safety, we verify the opportunity ID exists in our input list
                matched_opp = next((o for o in opportunities if str(o.id) == item.get('opportunity_id')), None)
                
                # If LLM hallucinated an ID or we want to use the first one as fallback (rare)
                if not matched_opp and len(opportunities) > 0:
                     # Fallback logic or skip
                     pass

                if matched_opp:
                    exp = Experiment(
                        user_id=user_id,
                        opportunity_id=matched_opp.id,
                        type=item.get("type", "learning"),
                        hypothesis=item.get("hypothesis", "Test skill"),
                        belief_id=item.get("belief_target"),
                        status="proposed",
                        meta_data={"company": matched_opp.company, "role": matched_opp.title, "url": matched_opp.url}
                    )
                    experiments.append(exp)
            
            logger.info(f"Generated {len(experiments)} experiments.")
            return experiments

        except Exception as e:
            logger.error(f"Planning failed: {e}")
            return []
