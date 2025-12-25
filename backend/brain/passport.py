from typing import List, Dict
import uuid
from backend.models import (
    ResumeEvidence, GitHubEvidence, LinkedInEvidence, 
    BeliefState, Belief, BeliefUpdate
)

# Configuration for heuristics (Plan to move to LLM later, keeping procedural for stability)
CONFIDENCE_SCORES = {
    "resume_claim": 0.3,   # Claiming it on a resume is low signal
    "linkedin_skill": 0.1, # Endorsements/claims are low signal
    "github_primary_lang": 0.4, # Used in a repo is decent signal
    "github_star_bonus": 0.1,   # If it's a popular repo
}

class PassportGenerator:
    def __init__(self):
        # Placeholder for LLM client ("APIHERE")
        self.llm_api_key = "APIHERE" 
    
    def generate_initial_passport(
        self, 
        user_id: uuid.UUID, 
        resume: ResumeEvidence = None, 
        github: GitHubEvidence = None, 
        linkedin: LinkedInEvidence = None
    ) -> BeliefState:
        """
        Synthesizes raw evidence into a coherent BeliefState (The Failure Passport).
        """
        beliefs: Dict[str, Belief] = {}

        # 1. Process Resume
        if resume:
            for skill in resume.skills:
                attr = skill.name
                if attr not in beliefs:
                    beliefs[attr] = Belief(
                        attribute=attr, 
                        confidence=0.0, 
                        basis="Initial Discovery"
                    )
                
                # Update confidence
                beliefs[attr].confidence = min(1.0, beliefs[attr].confidence + CONFIDENCE_SCORES["resume_claim"])
                beliefs[attr].history.append(BeliefUpdate(
                    old_confidence=0.0, # Approximate
                    new_confidence=beliefs[attr].confidence,
                    reason=f"Claimed on Resume (Exp: {skill.years_of_experience} yrs)"
                ))

        # 2. Process GitHub
        if github:
            # Analyze top repos
            for repo in github.top_repositories:
                if not repo.primary_language:
                    continue
                
                attr = repo.primary_language
                # Normalize name if needed (e.g. "py" -> "Python") - skipping for MVP
                
                if attr not in beliefs:
                    beliefs[attr] = Belief(attribute=attr, confidence=0.0, basis="GitHub Discovery")
                
                old_conf = beliefs[attr].confidence
                bonus = CONFIDENCE_SCORES["github_primary_lang"]
                if repo.stars > 5:
                    bonus += CONFIDENCE_SCORES["github_star_bonus"]
                
                beliefs[attr].confidence = min(1.0, old_conf + bonus)
                beliefs[attr].history.append(BeliefUpdate(
                    old_confidence=old_conf,
                    new_confidence=beliefs[attr].confidence,
                    reason=f"Used in GitHub Repo '{repo.name}' ({repo.stars} stars)"
                ))

        # 3. Process LinkedIn
        if linkedin:
            for skill in linkedin.skills:
                attr = skill
                if attr not in beliefs:
                    beliefs[attr] = Belief(attribute=attr, confidence=0.0, basis="LinkedIn Discovery")
                
                old_conf = beliefs[attr].confidence
                beliefs[attr].confidence = min(1.0, old_conf + CONFIDENCE_SCORES["linkedin_skill"])
                # No history update for minor bump to reduce noise, or add if critical.
        
        return BeliefState(
            user_id=user_id,
            beliefs=beliefs
        )
