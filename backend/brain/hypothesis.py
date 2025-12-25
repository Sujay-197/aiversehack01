from typing import List, Dict, Set, Tuple
import uuid
import json
from backend.models import BeliefState, Opportunity, Experiment
from backend.llm.client import LLMClient
from backend.config import config

class HypothesisGenerator:
    """
    Generates experiments by matching Beliefs (User) to Opportunities (Market).
    Uses Dynamic Semantic Matching via LLM.
    """

    def __init__(self):
        self.llm = LLMClient()

    def _get_semantic_matches(self, requirements: Set[str], beliefs: Set[str]) -> Dict[str, str]:
        """
        Ask LLM to find semantic matches between Job Requirements and User Beliefs.
        Returns a map: {requirement: matched_belief_attribute}
        """
        if not requirements or not beliefs:
            return {}

        prompt = f"""
You are a semantic matcher for a career agent.
Match Job Requirements to User Skills even if names differ (e.g. "RDBMS" matches "PostgreSQL").

Job Requirements: {list(requirements)}
User Skills: {list(beliefs)}

Return a JSON mapping ONLY for valid semantic matches.
Format: {{"Job Requirement": "User Skill"}}
"""
        try:
            response = self.llm.generate(prompt, json_response=True)
            matches = self.llm.parse_json_response(response)
            return matches
        except Exception as e:
            print(f"[Hypothesis Error] Semantic matching failed: {e}")
            return {}

    def generate_experiments(self, belief_state: BeliefState, opportunities: List[Opportunity]) -> List[Experiment]:
        """
        The Scientist Core: Matches what we believe (Passport) with what we can test (Market).
        Returns a list of proposed Experiments.
        """
        experiments = []
        user_id = belief_state.user_id
        beliefs_map = belief_state.beliefs
        user_skills = set(beliefs_map.keys())
        
        # 1. Gather all requirements to batch match (Optimization)
        # Note: For strict "per-opportunity" context, we might want to do this per opp or batch all.
        # For MVP, let's do per-opportunity to keep context clear or batch if list is huge.
        # Let's do it per opportunity for accuracy, but it's slower.
        
        for opp in opportunities:
            # Get semantic matches for this specific opportunity
            opp_reqs = set(opp.requirements)
            
            # Direct string matches first (Cheap)
            matched_map = {} # {req: belief_obj}
            unmatched_reqs = set()
            
            for req in opp_reqs:
                # Direct match check
                found_belief = None
                req_lower = req.lower()
                for attr, belief in beliefs_map.items():
                    if req_lower in attr.lower() or attr.lower() in req_lower:
                        found_belief = belief
                        break
                
                if found_belief:
                    matched_map[req] = found_belief
                else:
                    unmatched_reqs.add(req)
            
            # Dynamic Semantic Match for leftovers (LLM)
            if unmatched_reqs:
                # Only ask LLM if we have unmatched requirements and beliefs to check against
                # Filter out beliefs we already matched to avoid duplicate checks? No, one skill can match multiple reqs.
                semantic_map = self._get_semantic_matches(unmatched_reqs, user_skills)
                
                for req, matched_skill_name in semantic_map.items():
                    if matched_skill_name in beliefs_map:
                         matched_map[req] = beliefs_map[matched_skill_name]

            # Collect matches and missing
            matched_beliefs_list = list(matched_map.values())
            missing_skills = [r for r in opp_reqs if r not in matched_map] # Re-calc missing

            # DECISION LOGIC
            
            # Calculate stats
            avg_conf = 0.0
            max_conf = 0.0
            if matched_beliefs_list:
                confs = [b.confidence for b in matched_beliefs_list]
                avg_conf = sum(confs) / len(confs)
                max_conf = max(confs)

            # Case 1: Verification (Anchor Skill is Strong)
            if len(matched_beliefs_list) > 0 and max_conf > config.THRESHOLDS.VERIFICATION_CONFIDENCE_THRESHOLD:
                exp_type = "verification"
                
                missing_str = f" despite missing {missing_skills}" if missing_skills else ""
                hypothesis = f"High Confidence ({avg_conf:.2f}). Expecting Interview{missing_str}."
                    
                experiments.append(Experiment(
                    user_id=user_id,
                    belief_id=matched_beliefs_list[0].attribute, # Primary skill being tested
                    opportunity_id=opp.id,
                    type=exp_type,
                    hypothesis=hypothesis
                ))

            # Case 2: Partial/Weak Match (Learning)
            elif len(matched_beliefs_list) > 0:
                experiments.append(Experiment(
                    user_id=user_id,
                    belief_id=matched_beliefs_list[0].attribute,
                    opportunity_id=opp.id,
                    type="learning",
                    hypothesis=f"Weak Match ({avg_conf:.2f}). Testing if this is enough."
                ))
            
            # Case 3: Moonshot (Not implemented yet)
            
        return experiments
