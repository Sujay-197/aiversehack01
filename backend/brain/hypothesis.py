from typing import List, Dict
import uuid
from backend.models import BeliefState, Opportunity, Experiment

class HypothesisGenerator:
    # Simple ontology for semantic matching
    SKILL_ONTOLOGY = {
        "PostgreSQL": ["SQL", "Database", "RDBMS"],
        "Python": ["Django", "Flask", "FastAPI", "Scripting"],
        "React": ["JavaScript", "Frontend", "UI", "Web"],
        "JavaScript": ["React", "Vue", "Node", "Frontend", "Web"],
        "Git": ["Version Control", "GitHub", "GitLab"]
    }

    def generate_experiments(self, belief_state: BeliefState, opportunities: List[Opportunity]) -> List[Experiment]:
        """
        The Scientist Core: Matches what we believe (Passport) with what we can test (Market).
        Returns a list of proposed Experiments.
        """
        experiments = []
        user_id = belief_state.user_id
        beliefs = belief_state.beliefs
        
        for opp in opportunities:
            # Simple keyword matching logic for MVP (Tag Matching)
            
            matched_skills = []
            missing_skills = []
            
            for req in opp.requirements:
                found = False
                req_lower = req.lower()

                for attr, belief in beliefs.items():
                    attr_lower = attr.lower()
                    
                    # 1. Direct Match
                    if req_lower in attr_lower or attr_lower in req_lower:
                        matched_skills.append(belief)
                        found = True
                        break
                    
                    # 2. Ontology Match
                    related = self.SKILL_ONTOLOGY.get(attr, [])
                    if any(r.lower() == req_lower for r in related):
                        matched_skills.append(belief)
                        found = True
                        break
                        
                if not found:
                    missing_skills.append(req)
            
            # DECISION LOGIC
            
            # Calculate stats
            avg_conf = 0.0
            max_conf = 0.0
            if matched_skills:
                confs = [b.confidence for b in matched_skills]
                avg_conf = sum(confs) / len(confs)
                max_conf = max(confs)

            # Case 1: Verification (Anchor Skill is Strong)
            # If our strongest matched skill is High Confidence (>0.7), we are verifying that strength.
            if len(matched_skills) > 0 and max_conf > 0.7:
                exp_type = "verification"
                
                missing_str = f" despite missing {missing_skills}" if missing_skills else ""
                hypothesis = f"High Confidence ({avg_conf:.2f}). Expecting Interview{missing_str}."
                    
                experiments.append(Experiment(
                    user_id=user_id,
                    belief_id=matched_skills[0].attribute, # Primary skill being tested
                    opportunity_id=opp.id,
                    type=exp_type,
                    hypothesis=hypothesis
                ))

            # Case 2: Partial/Weak Match (Low confidence in matched skills)
            # We are "Learning" if our current beliefs are justified.
            elif len(matched_skills) > 0:
                experiments.append(Experiment(
                    user_id=user_id,
                    belief_id=matched_skills[0].attribute,
                    opportunity_id=opp.id,
                    type="learning",
                    hypothesis=f"Weak Match ({avg_conf:.2f}). Testing if this is enough."
                ))
            
            # Case 3: Moonshot (We have skills but they are low confidence, AND we might be missing some)
            # Or assume missing skills = 0 confidence.
            
        return experiments
