from typing import List, Dict
from datetime import datetime
import uuid
from backend.models import BeliefState, Belief, BeliefUpdate

class PassportGenerator:
    """
    Generates the initial BeliefState (Failure Passport) from evidence.
    
    REVISED SCORING RULES (Post-Evaluation v2):
    - Confidence capped by source type (no cumulative inflation)
    - Years tracked for experience validation  
    - Context inferred for domain matching
    """
    
    def generate_initial_passport(
        self, 
        user_id: uuid.UUID, 
        resume=None, 
        github=None, 
        linkedin=None
    ) -> BeliefState:
        beliefs: Dict[str, Belief] = {}
        
        # Infer primary context from resume
        primary_context = "General"
        if resume and resume.work_experience:
            latest_job = resume.work_experience[0] if isinstance(resume.work_experience, list) else {}
            job_title = latest_job.get("title", "").lower()
            
            if any(kw in job_title for kw in ["backend", "api", "server"]):
                primary_context = "Backend Engineering"
            elif any(kw in job_title for kw in ["frontend", "react", "ui"]):
                primary_context = "Frontend Engineering"
            elif any(kw in job_title for kw in ["data", "analyst", "analytics"]):
                primary_context = "Data Analytics"
            elif any(kw in job_title for kw in ["ml", "ai", "research"]):
                primary_context = "ML/AI"
        
        # 1. Process Resume (Primary source for years + context)
        if resume:
            for skill in resume.skills:
                attr = skill.name
                years = skill.years_of_experience
                
                # Confidence from years (capped at 0.45 to avoid inflation)
                resume_conf = min(0.45, 0.15 + (years * 0.06))
                
                beliefs[attr] = Belief(
                    attribute=attr,
                    confidence=resume_conf,
                    basis=f"Resume ({years:.1f} years)",
                    years_of_experience=years,
                    work_years=years,  # Professional experience
                    context=primary_context
                )
                beliefs[attr].history.append(BeliefUpdate(
                    old_confidence=0.0,
                    new_confidence=resume_conf,
                    reason=f"Claimed on Resume (Exp: {years:.1f} yrs)",
                    timestamp=datetime.now()
                ))
        
        # 2. Process GitHub (cap at 0.35)
        if github:
            for repo in github.top_repositories:
                if not repo.primary_language:
                    continue
                
                attr = repo.primary_language
                
                # Base: 0.15, Stars bonus capped
                github_conf = 0.15 + min(0.20, (repo.stars / 20) * 0.05)
                
                # Infer context
                repo_context = primary_context
                desc = (repo.description or "").lower()
                if any(kw in desc for kw in ["backend", "api", "server"]):
                    repo_context = "Backend Engineering"
                elif any(kw in desc for kw in ["ml", "ai", "pytorch"]):
                    repo_context = "ML/AI"
                
                if attr not in beliefs:
                    beliefs[attr] = Belief(
                        attribute=attr,
                        confidence=github_conf,
                        basis=f"GitHub ({repo.stars} stars)",
                        years_of_experience=0.5,  # Project experience
                        work_years=0.0,  # NOT professional work
                        context=repo_context
                    )
                else:
                    # Take MAX confidence
                    if github_conf > beliefs[attr].confidence:
                        beliefs[attr].confidence = github_conf
                    # Accumulate skill years (projects count for practice)
                    beliefs[attr].years_of_experience += 0.5
                    # work_years stays the same (GitHub != professional work)
                
                beliefs[attr].history.append(BeliefUpdate(
                    old_confidence=beliefs[attr].confidence - github_conf if github_conf > beliefs[attr].confidence else 0,
                    new_confidence=beliefs[attr].confidence,
                    reason=f"Used in GitHub Repo '{repo.name}' ({repo.stars} stars)",
                    timestamp=datetime.now()
                ))
        
        # 3. LinkedIn (small boost only)
        if linkedin:
            for skill in linkedin.skills:
                if skill in beliefs:
                    old_conf = beliefs[skill].confidence
                    beliefs[skill].confidence = min(1.0, old_conf + 0.05)
                    beliefs[skill].history.append(BeliefUpdate(
                        old_confidence=old_conf,
                        new_confidence=beliefs[skill].confidence,
                        reason="Endorsed on LinkedIn",
                        timestamp=datetime.now()
                    ))
                else:
                    beliefs[skill] = Belief(
                        attribute=skill,
                        confidence=0.10,
                        basis="LinkedIn",
                        years_of_experience=0.0,
                        context="General"
                    )
        
        return BeliefState(user_id=user_id, beliefs=beliefs)
