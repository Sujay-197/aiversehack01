"""
Comparison Test: Old vs New Agent Performance

This test runs the SAME personas through BOTH graph versions to demonstrate improvements.
"""
import sys
import os
sys.path.append(os.getcwd())

from backend.models import Opportunity
from backend.brain.passport import PassportGenerator
from backend.brain.passport_v2 import PassportGenerator as PassportGeneratorV2
from backend.brain.graph import build_graph
from backend.brain.graph_v2 import build_graph_v2
from test_evaluation import PersonaFactory

def compare_versions():
    print("="*80)
    print("COMPARISON TEST: Old vs New Agent")
    print("="*80)
    
    factory = PersonaFactory()
    
    # Test opportunities
    opportunities = [
        Opportunity(
            title="Staff Backend Engineer",
            company="TechGiant",
            url="https://techgiant.com/staff",
            type="job",
            requirements=["Python", "System Design", "AWS", "Leadership"],
            source="test"
        ),
        Opportunity(
            title="Junior Software Engineer",
            company="MidCorp",
            url="https://midcorp.com/junior",
            type="internship",
            requirements=["Python", "Git", "Algorithms"],
            source="test"
        ),
        Opportunity(
            title="ML Research Engineer",
            company="AI Lab",
            url="https://ailab.com/ml",
            type="job",
            requirements=["Python", "PyTorch", "Research"],
            source="test"
        ),
    ]
    
    # Test persona: Fresh Graduate
    user_id, resume, github, linkedin, name = factory.fresh_graduate()
    
    print(f"\n[TEST PERSONA] {name}")
    print(f"Profile: 2 years Python (academic), 1 hackathon project (5 stars)")
    print("-"*80)
    
    # OLD VERSION
    print("\n### OLD VERSION (No Filtering) ###\n")
    passport_old = PassportGenerator().generate_initial_passport(user_id, resume, github, linkedin)
    print(f"Python Confidence: {passport_old.beliefs['Python'].confidence:.2f}")
    print(f"Python Years: {passport_old.beliefs['Python'].years_of_experience:.1f}")
    
    graph_old = build_graph()
    old_experiments = []
    
    for opp in opportunities:
        result = graph_old.invoke({
            "user_id": user_id,
            "opportunity": opp,
            "belief_state": passport_old,
            "relevant_beliefs": [],
            "proposed_experiment": None
        })
        exp = result["proposed_experiment"]
        if exp:
            old_experiments.append((exp, opp))
            print(f"  [{exp.type.upper()}] {opp.title}")
    
    print(f"\nTotal Proposals: {len(old_experiments)}/3")
    
    # NEW VERSION
    print("\n### NEW VERSION (With Filtering) ###\n")
    passport_new = PassportGeneratorV2().generate_initial_passport(user_id, resume, github, linkedin)
    print(f"Python Confidence: {passport_new.beliefs['Python'].confidence:.2f}")
    print(f"Python Years: {passport_new.beliefs['Python'].years_of_experience:.1f}")
    print(f"Python Context: {passport_new.beliefs['Python'].context}")
    
    graph_new = build_graph_v2()
    new_experiments = []
    
    for opp in opportunities:
        result = graph_new.invoke({
            "user_id": user_id,
            "opportunity": opp,
            "belief_state": passport_new,
            "relevant_beliefs": [],
            "proposed_experiment": None
        })
        exp = result.get("proposed_experiment")
        # Only count if not filtered
        if exp and not result.get("_filtered", False):
            new_experiments.append((exp, opp))
            print(f"  [{exp.type.upper()}] {opp.title}")
            print(f"      {exp.hypothesis}")
    
    print(f"\nTotal Proposals: {len(new_experiments)}/3")
    
    # ANALYSIS
    print("\n" + "="*80)
    print("COMPARISON RESULTS")
    print("="*80)
    
    print(f"\n1. Confidence Inflation Fix:")
    print(f"   Old: {passport_old.beliefs['Python'].confidence:.2f} (from 5-star hackathon)")
    print(f"   New: {passport_new.beliefs['Python'].confidence:.2f} (capped scoring)")
    
    improvement_1 = "FIXED" if passport_new.beliefs['Python'].confidence < 0.5 else "NEEDS WORK"
    print(f"   Status: {improvement_1}")
    
    print(f"\n2. Selectivity:")
    old_selectivity = 1 - (len(old_experiments) / 3)
    new_selectivity = 1 - (len(new_experiments) / 3)
    print(f"   Old: {old_selectivity:.1%} (applied to {len(old_experiments)}/3)")
    print(f"   New: {new_selectivity:.1%} (applied to {len(new_experiments)}/3)")
    
    improvement_2 = "IMPROVED" if new_selectivity > old_selectivity else "NO CHANGE"
    print(f"   Status: {improvement_2}")
    
    print(f"\n3. Specific Checks:")
    
    # Check 1: Did old version apply to Staff role?
    old_staff = any("Staff" in o.title for e, o in old_experiments)
    new_staff = any("Staff" in o.title for e, o in new_experiments)
    print(f"   Graduate -> Staff Role:")
    print(f"      Old: {'Applied [X]' if old_staff else 'Skipped [OK]'}")
    print(f"      New: {'Applied [X]' if new_staff else 'Skipped [OK]'}")
    
    # Check 2: Did old version apply to ML role?
    old_ml = any("ML" in o.title or "Research" in o.title for e, o in old_experiments)
    new_ml = any("ML" in o.title or "Research" in o.title for e, o in new_experiments)
    print(f"   Graduate -> ML Research Role:")
    print(f"      Old: {'Applied [X]' if old_ml else 'Skipped [OK]'}")
    print(f"      New: {'Applied [X]' if new_ml else 'Skipped [OK]'}")
    
    # Final Grade
    fixes = 0
    if improvement_1 == "FIXED":
        fixes += 1
    if improvement_2 == "IMPROVED":
        fixes += 1
    if not new_staff:
        fixes += 1
    if not new_ml:
        fixes += 1
    
    grade = "A" if fixes >= 3 else "B" if fixes >= 2 else "C"
    
    print(f"\n{'='*80}")
    print(f"IMPROVEMENT GRADE: {grade} ({fixes}/4 issues fixed)")
    print(f"{'='*80}")

if __name__ == "__main__":
    compare_versions()
