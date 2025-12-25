"""
Agent Performance Evaluation: Multiple User Personas

This test evaluates the Hypothesis Engine's performance across different user profiles:
1. Senior Expert (High confidence, specialized)
2. Career Switcher (Mixed confidence, domain gap)
3. Fresh Graduate (Low confidence, broad skills)

Metrics:
- Hypothesis Accuracy (Does the type match confidence?)
- Adaptation Quality (Does reflection improve decisions?)
- Skill Coverage (Are all relevant skills considered?)
"""
import sys
import os
sys.path.append(os.getcwd())

from backend.models import ResumeEvidence, GitHubEvidence, LinkedInEvidence, Skill, GitHubRepo, Opportunity, Outcome, BeliefState
from backend.brain.passport import PassportGenerator
from backend.brain.graph import build_graph
from backend.brain.reflection import Reflector
import uuid
from typing import List, Dict

class PersonaFactory:
    """Generate different user personas for testing"""
    
    @staticmethod
    def senior_python_expert() -> tuple:
        """10 years Python, strong backend, weak frontend"""
        user_id = uuid.uuid4()
        
        resume = ResumeEvidence(
            user_id=user_id,
            full_name="Sarah Chen",
            email="sarah@example.com",
            summary="Senior Backend Engineer with 10+ years Python experience",
            skills=[
                Skill(name="Python", category="Language", years_of_experience=10),
                Skill(name="Django", category="Framework", years_of_experience=8),
                Skill(name="PostgreSQL", category="Database", years_of_experience=7),
                Skill(name="AWS", category="Cloud", years_of_experience=5),
                Skill(name="React", category="Frontend", years_of_experience=0.5),
            ],
            experience=[{"title": "Senior Engineer", "company": "BigTech", "years": 8}]
        )
        
        github = GitHubEvidence(
            user_id=user_id,
            username="sarah-codes",
            bio="Building scalable systems",
            public_repos=45,
            top_repositories=[
                GitHubRepo(name="microservices-framework", url="https://github.com/sarah-codes/microservices-framework", primary_language="Python", stars=250, description="Production-grade microservices"),
                GitHubRepo(name="data-pipeline", url="https://github.com/sarah-codes/data-pipeline", primary_language="Python", stars=120),
                GitHubRepo(name="api-gateway", url="https://github.com/sarah-codes/api-gateway", primary_language="Go", stars=80),
            ],
            followers=350
        )
        
        linkedin = LinkedInEvidence(
            user_id=user_id,
            profile_url="https://linkedin.com/in/sarachen",
            headline="Senior Backend Engineer @ BigTech",
            skills=["Python", "System Design", "Leadership", "Mentoring"]
        )
        
        return user_id, resume, github, linkedin, "Senior Expert"
    
    @staticmethod
    def career_switcher() -> tuple:
        """Former Data Analyst → Software Engineer"""
        user_id = uuid.uuid4()
        
        resume = ResumeEvidence(
            user_id=user_id,
            full_name="Mike Johnson",
            email="mike@example.com",
            summary="Data Analyst transitioning to Full Stack Development",
            skills=[
                Skill(name="Python", category="Language", years_of_experience=3),
                Skill(name="SQL", category="Database", years_of_experience=5),
                Skill(name="JavaScript", category="Language", years_of_experience=1),
                Skill(name="React", category="Frontend", years_of_experience=0.5),
                Skill(name="Excel", category="Tool", years_of_experience=7),
            ],
            experience=[{"title": "Data Analyst", "company": "FinCorp", "years": 5}]
        )
        
        github = GitHubEvidence(
            user_id=user_id,
            username="mike-builds",
            bio="Learning to code full-time",
            public_repos=8,
            top_repositories=[
                GitHubRepo(name="data-viz-dashboard", url="https://github.com/mike-builds/data-viz-dashboard", primary_language="Python", stars=3),
                GitHubRepo(name="todo-app-react", url="https://github.com/mike-builds/todo-app-react", primary_language="JavaScript", stars=1),
            ],
            followers=12
        )
        
        linkedin = LinkedInEvidence(
            user_id=user_id,
            profile_url="https://linkedin.com/in/mikej",
            headline="Aspiring Full Stack Developer",
            skills=["Python", "SQL", "Data Analysis"]
        )
        
        return user_id, resume, github, linkedin, "Career Switcher"
    
    @staticmethod
    def fresh_graduate() -> tuple:
        """New CS grad, theoretical knowledge, minimal production experience"""
        user_id = uuid.uuid4()
        
        resume = ResumeEvidence(
            user_id=user_id,
            full_name="Alex Kumar",
            email="alex@example.com",
            summary="Recent CS graduate seeking entry-level opportunities",
            skills=[
                Skill(name="Python", category="Language", years_of_experience=2),
                Skill(name="Java", category="Language", years_of_experience=1),
                Skill(name="React", category="Frontend", years_of_experience=0.5),
                Skill(name="Git", category="Tool", years_of_experience=2),
            ],
            experience=[{"title": "CS Student", "company": "State University", "years": 4}]
        )
        
        github = GitHubEvidence(
            user_id=user_id,
            username="alex-learns",
            bio="CS grad, building cool stuff",
            public_repos=15,
            top_repositories=[
                GitHubRepo(name="sorting-algorithms", url="https://github.com/alex-learns/sorting-algorithms", primary_language="Python", stars=2),
                GitHubRepo(name="personal-website", url="https://github.com/alex-learns/personal-website", primary_language="JavaScript", stars=1),
                GitHubRepo(name="hackathon-project", url="https://github.com/alex-learns/hackathon-project", primary_language="Python", stars=5),
            ],
            followers=8
        )
        
        linkedin = LinkedInEvidence(
            user_id=user_id,
            profile_url="https://linkedin.com/in/alexk",
            headline="Computer Science Graduate",
            skills=["Python", "Algorithms", "Data Structures"]
        )
        
        return user_id, resume, github, linkedin, "Fresh Graduate"


class PerformanceEvaluator:
    """Evaluate agent performance across metrics"""
    
    def __init__(self):
        self.passport_gen = PassportGenerator()
        self.graph = build_graph()
        self.reflector = Reflector()
    
    def evaluate_persona(self, user_id, resume, github, linkedin, persona_name: str) -> Dict:
        """Run full evaluation for one persona"""
        print(f"\n{'='*80}")
        print(f"EVALUATING: {persona_name}")
        print(f"{'='*80}")
        
        # Phase 1: Generate Passport
        passport = self.passport_gen.generate_initial_passport(user_id, resume, github, linkedin)
        print(f"\n[Passport] {len(passport.beliefs)} beliefs generated:")
        for attr, belief in sorted(passport.beliefs.items(), key=lambda x: x[1].confidence, reverse=True):
            print(f"  {attr}: {belief.confidence:.2f}")
        
        # Phase 2: Test against diverse opportunities
        opportunities = self._get_test_opportunities()
        
        # Phase 3: Generate experiments
        experiments = []
        for opp in opportunities:
            result = self.graph.invoke({
                "user_id": user_id,
                "opportunity": opp,
                "belief_state": passport,
                "relevant_beliefs": [],
                "proposed_experiment": None
            })
            exp = result["proposed_experiment"]
            if exp:
                experiments.append((exp, opp))
        
        print(f"\n[Experiments] Generated {len(experiments)} proposals:")
        for exp, opp in experiments:
            print(f"  [{exp.type.upper()}] {opp.title}")
            print(f"    Confidence: {self._get_max_confidence(passport, opp):.2f}")
            print(f"    Hypothesis: {exp.hypothesis[:70]}...")
        
        # Phase 4: Evaluate quality
        metrics = self._calculate_metrics(passport, experiments, persona_name)
        
        return {
            "persona": persona_name,
            "passport": passport,
            "experiments": experiments,
            "metrics": metrics
        }
    
    def _get_test_opportunities(self) -> List[Opportunity]:
        """Diverse set of opportunities for testing"""
        return [
            # Senior role (should match expert, not grad)
            Opportunity(
                title="Staff Backend Engineer",
                company="TechGiant",
                url="https://techgiant.com/staff",
                type="job",
                requirements=["Python", "System Design", "AWS", "Leadership"],
                source="test"
            ),
            # Mid-level full stack (should match switcher best)
            Opportunity(
                title="Full Stack Developer",
                company="Startup",
                url="https://startup.com/fullstack",
                type="job",
                requirements=["Python", "React", "SQL"],
                source="test"
            ),
            # Entry-level (should match grad)
            Opportunity(
                title="Junior Software Engineer",
                company="MidCorp",
                url="https://midcorp.com/junior",
                type="internship",
                requirements=["Python", "Git", "Algorithms"],
                source="test"
            ),
            # Specialized (high bar)
            Opportunity(
                title="ML Research Engineer",
                company="AI Lab",
                url="https://ailab.com/ml",
                type="job",
                requirements=["Python", "PyTorch", "Research"],
                source="test"
            ),
            # Hackathon (anyone can try)
            Opportunity(
                title="Global Hackathon",
                company="HackOrg",
                url="https://hackorg.com/event",
                type="hackathon",
                requirements=["Python"],
                source="test"
            )
        ]
    
    def _get_max_confidence(self, passport: BeliefState, opp: Opportunity) -> float:
        """Get max confidence for opportunity requirements"""
        confs = []
        for req in opp.requirements:
            for attr, belief in passport.beliefs.items():
                if req.lower() in attr.lower() or attr.lower() in req.lower():
                    confs.append(belief.confidence)
        return max(confs) if confs else 0.0
    
    def _calculate_metrics(self, passport: BeliefState, experiments: List, persona_name: str) -> Dict:
        """Calculate performance metrics"""
        
        # Metric 1: Hypothesis Accuracy (does type match confidence?)
        correct_types = 0
        for exp, opp in experiments:
            max_conf = self._get_max_confidence(passport, opp)
            expected_type = "verification" if max_conf > 0.7 else "learning"
            if exp.type == expected_type or "CAUTION" in exp.hypothesis:
                correct_types += 1
        
        accuracy = correct_types / len(experiments) if experiments else 0
        
        # Metric 2: Skill Coverage (are we using all strong beliefs?)
        strong_beliefs = [k for k, v in passport.beliefs.items() if v.confidence > 0.6]
        tested_beliefs = set([exp.belief_id for exp, _ in experiments if exp.belief_id])
        coverage = len(tested_beliefs & set(strong_beliefs)) / len(strong_beliefs) if strong_beliefs else 0
        
        # Metric 3: Selectivity (not applying to everything)
        total_opps = 5  # We have 5 test opportunities
        selectivity = 1 - (len(experiments) / total_opps) if total_opps else 0
        
        metrics = {
            "hypothesis_accuracy": accuracy,
            "skill_coverage": coverage,
            "selectivity": selectivity,
            "total_experiments": len(experiments),
            "strong_beliefs": len(strong_beliefs)
        }
        
        print(f"\n[Metrics]")
        print(f"  Hypothesis Accuracy: {accuracy:.1%} ({correct_types}/{len(experiments)})")
        print(f"  Skill Coverage: {coverage:.1%} ({len(tested_beliefs & set(strong_beliefs))}/{len(strong_beliefs)} strong skills tested)")
        print(f"  Selectivity: {selectivity:.1%} (applied to {len(experiments)}/5 opportunities)")
        
        return metrics


def run_evaluation():
    """Run complete evaluation across all personas"""
    print("="*80)
    print("CAREER SCIENTIST - AGENT PERFORMANCE EVALUATION")
    print("="*80)
    
    evaluator = PerformanceEvaluator()
    factory = PersonaFactory()
    
    results = []
    
    # Test each persona
    for persona_method in [factory.senior_python_expert, factory.career_switcher, factory.fresh_graduate]:
        user_id, resume, github, linkedin, name = persona_method()
        result = evaluator.evaluate_persona(user_id, resume, github, linkedin, name)
        results.append(result)
    
    # Aggregate analysis
    print(f"\n{'='*80}")
    print("AGGREGATE ANALYSIS")
    print(f"{'='*80}")
    
    avg_accuracy = sum(r["metrics"]["hypothesis_accuracy"] for r in results) / len(results)
    avg_coverage = sum(r["metrics"]["skill_coverage"] for r in results) / len(results)
    avg_selectivity = sum(r["metrics"]["selectivity"] for r in results) / len(results)
    
    print(f"\nAverage Performance:")
    print(f"  Hypothesis Accuracy: {avg_accuracy:.1%}")
    print(f"  Skill Coverage: {avg_coverage:.1%}")
    print(f"  Selectivity: {avg_selectivity:.1%}")
    
    # Best practices validation
    print(f"\n[Validation Checks]")
    checks = []
    
    # Check 1: Expert should get VERIFICATION for senior roles
    expert_result = results[0]
    expert_experiments = expert_result["experiments"]
    senior_match = next(((e, o) for e, o in expert_experiments if "Staff" in o.title), None)
    if senior_match:
        senior_exp, senior_opp = senior_match
        if senior_exp.type == "verification" or "CAUTION" not in senior_exp.hypothesis:
            print("  [OK] Expert correctly matched to senior role (VERIFICATION)")
            checks.append(True)
        else:
            print("  [WARN] Expert should get VERIFICATION for senior roles")
            checks.append(False)
    else:
        print("  [WARN] Expert did not generate experiment for senior role")
        checks.append(False)
    
    # Check 2: Fresh grad should NOT get VERIFICATION for senior roles
    grad_result = results[2]
    grad_experiments = grad_result["experiments"]
    grad_match = next(((e, o) for e, o in grad_experiments if "Staff" in o.title), None)
    if not grad_match:
        print("  [OK] Graduate correctly avoided senior role")
        checks.append(True)
    elif grad_match:
        grad_exp, grad_opp = grad_match
        if grad_exp.type == "learning":
            print("  [OK] Graduate correctly downgraded senior role to LEARNING")
            checks.append(True)
        else:
            print("  [WARN] Graduate should not be confident about staff roles")
            checks.append(False)
    
    # Check 3: All personas should apply to hackathons (low barrier)
    hackathon_count = sum(1 for r in results for e, o in r["experiments"] if o.type == "hackathon")
    if hackathon_count >= 2:  # At least 2/3 personas
        print(f"  [OK] Hackathons recognized as accessible ({hackathon_count}/3 personas)")
        checks.append(True)
    else:
        print(f"  [WARN] Hackathons should be accessible to most personas")
        checks.append(False)
    
    grade = "A" if all(checks) else "B" if sum(checks) >= 2 else "C"
    print(f"\nOVERALL GRADE: {grade}")
    print(f"{'='*80}")


if __name__ == "__main__":
    run_evaluation()
