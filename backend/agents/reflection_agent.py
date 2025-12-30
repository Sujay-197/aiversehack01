
import logging
from typing import List, Dict
from textwrap import dedent
import json
from google import genai
from backend.config import config
from backend.models import BeliefState, Experiment, Outcome, Belief, BeliefUpdate

# Configure Logging
logger = logging.getLogger("ReflectionAgent")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class ReflectionAgent:
    """
    The Scientist's Notebook.
    Analyzes Experiment Outcomes -> Updates Belief State.
    """
    def __init__(self):
        self.api_key = config.GEMINI_API_KEY
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not set. Reflection will fail.")
            self.client = None
        else:
            self.client = genai.Client(api_key=self.api_key)
        self.model = config.LLM.MODEL_NAME

    def reflect(self, belief_state: BeliefState, experiment: Experiment, outcome: Outcome) -> BeliefState:
        """
        Updates the belief state based on the experiment outcome.
        Returns the MODIFIED belief state (in-place modification is fine, but we return it for clarity).
        """
        
        # 1. Identify valid target belief
        target_belief_name = experiment.belief_id
        if not target_belief_name or target_belief_name not in belief_state.beliefs:
            logger.warning(f"Experiment targeted unknown belief '{target_belief_name}'. skipping specific update.")
            # Could prompt LLM to find the closest belief, but for now strict.
            return belief_state

        target_belief = belief_state.beliefs[target_belief_name]

        # 2. Construct Prompt
        prompt = dedent(f"""
        You are a Bayesian Career Scientist. Update the User's belief confidence based on new evidence.

        CURRENT BELIEF:
        - Skill: {target_belief_name}
        - Confidence: {target_belief.confidence} (0.0 to 1.0)
        - Context: {target_belief.context}

        EXPERIMENT:
        - Hypothesis: {experiment.hypothesis}
        - Type: {experiment.type}

        OUTCOME:
        - Result: {outcome.result}
        - Feedback: {outcome.feedback}

        TASK:
        Determine the new confidence score.
        - If success/offer: Confidence should significantly increase (towards 1.0).
        - If rejection w/ interview: Confidence might decrease slightly, or specific gaps identified.
        - If ghosted/no-reply: Small decrease (market noise).
        
        OUTPUT JSON:
        {{
            "new_confidence": float,
            "reasoning": "string explanation of the update",
            "suggested_next_step": "string (optional)"
        }}
        """).strip()

        try:
            logger.info(f"Reflecting on outcome for '{target_belief_name}'...")
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )

            raw_text = response.text
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "").replace("```", "")
            
            result = json.loads(raw_text)
            
            # 3. Apply Update
            new_conf = float(result.get("new_confidence", target_belief.confidence))
            reason = result.get("reasoning", "Automated update")
            
            # Clamp
            new_conf = max(0.0, min(1.0, new_conf))
            
            # Record Update History
            update_record = BeliefUpdate(
                old_confidence=target_belief.confidence,
                new_confidence=new_conf,
                reason=reason
            )
            
            # Update State
            target_belief.confidence = new_conf
            target_belief.history.append(update_record)
            
            # Version bump
            belief_state.version += 1
            
            logger.info(f"Belief '{target_belief_name}' updated: {update_record.old_confidence} -> {new_conf}")
            return belief_state

        except Exception as e:
            logger.error(f"Reflection failed: {e}")
            return belief_state
