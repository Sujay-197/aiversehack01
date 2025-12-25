# Agent Performance Evaluation Report

## Executive Summary

**Grade: B**  
**Date**: 2025-12-25  
**Evaluator**: Automated Test Suite

The Career Scientist hypothesis engine was tested across 3 distinct personas:
1. **Senior Expert** (10 years Python, strong backend)
2. **Career Switcher** (Data Analyst → Full Stack)
3. **Fresh Graduate** (CS grad, minimal production experience)

---

## Quantitative Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Hypothesis Accuracy | 100% | >90% | ✓ PASS |
| Skill Coverage | 83.3% | >70% | ✓ PASS |
| Selectivity | 0% | >30% | ✗ FAIL |

### Metric Definitions

- **Hypothesis Accuracy**: Does experiment type (VERIFICATION/LEARNING) match confidence level?
- **Skill Coverage**: Are high-confidence skills being tested?
- **Selectivity**: Does the agent avoid obviously bad-fit opportunities?

---

## Detailed Findings

### 1. Senior Expert (Sarah Chen)

**Profile**:
- 10 years Python, 8 years Django
- 250-star GitHub repo
- Confidence: Python (0.95), Django (0.90), PostgreSQL (0.80)

**Results**:
```
Generated 5 experiments:
- [VERIFICATION] Staff Backend Engineer ✓
- [VERIFICATION] Full Stack Developer ✓ 
- [VERIFICATION] Junior Software Engineer ⚠️ (overqualified)
- [VERIFICATION] ML Research Engineer ⚠️ (different domain)
- [VERIFICATION] Global Hackathon ✓
```

**Analysis**:
✓ Correctly matched senior role with VERIFICATION  
✓ High-confidence skills properly utilized  
⚠️ Applied to junior roles (should skip/deprioritize)  
⚠️ Applied to ML role despite no ML evidence

---

### 2. Career Switcher (Mike Johnson)

**Profile**:
- 3 years Python (analytics context)
- 5 years SQL, 1 year JavaScript
- Confidence: Python (0.80), JavaScript (0.70), SQL (0.40)

**Results**:
```
Generated 5 experiments:
- [VERIFICATION] Staff Backend Engineer ✗ (too senior)
- [VERIFICATION] Full Stack Developer ✓
- [VERIFICATION] Junior Software Engineer ✓
- [VERIFICATION] ML Research Engineer ✗ (wrong domain)
- [VERIFICATION] Global Hackathon ✓
```

**Analysis**:
✓ Full Stack match appropriate  
✗ **Should NOT** apply to Staff role (no system design, leadership evidence)  
✗ Applied to ML without relevant background

---

### 3. Fresh Graduate (Alex Kumar)

**Profile**:
- 2 years Python (academic)
- Hackathon project with 5 stars
- Confidence: Python (1.00), React (0.30), Git (0.30)

**Results**:
```
Generated 5 experiments:
- [VERIFICATION] Staff Backend Engineer ✗✗ CRITICAL BUG
- [VERIFICATION] Full Stack Developer ✗ (too senior)
- [VERIFICATION] Junior Software Engineer ✓
- [VERIFICATION] ML Research Engineer ✗ (requires PhD)
- [VERIFICATION] Global Hackathon ✓
```

**Analysis**:
✗✗ **CRITICAL**: Fresh grad has 1.00 confidence in Python, leading to VERIFICATION for Staff role  
✗ No experience filtering  
✗ No seniority awareness

---

## Root Cause Analysis

### Issue 1: Selectivity = 0% (Applied to ALL opportunities)

**Problem**: No filtering mechanism excludes poor-fit opportunities.

**Current Logic**:
```python
if max_conf > 0.7:
    return VERIFICATION experiment
```

**Missing**:
- Years of experience check
- Domain match (backend vs ML)
- Seniority level (junior/mid/senior/staff)

**Fix Needed**:
```python
if max_conf > 0.7 AND seniority_match AND domain_match:
    return VERIFICATION
else if opportunity_is_accessible:
    return LEARNING
else:
    return None  # Skip this opportunity
```

---

### Issue 2: Confidence Inflation (Fresh Grad = 1.00 Python)

**Problem**: GitHub star bonuses max out confidence too easily.

**Current Scoring**:
- Resume claim: +0.15
- GitHub primary language: +0.25
- GitHub 5+ stars: +0.15
- **Total**: 0.15 + 0.25 + 0.15 + 0.15 + 0.15 = 1.00

**Issue**: 5-star hackathon project ≠ 10 years production experience

**Fix Needed**:
- Cap GitHub contribution at 0.50
- Require YEARS validation (e.g., `years_of_experience > 5` for 0.9+ confidence)
- Differentiate between "I can code Python" vs "I can architect systems"

---

### Issue 3: No Context Awareness

**Problem**: "Python" for Data Analysis ≠ "Python" for Backend Engineering

**Example**: Mike (Career Switcher) has Python confidence from analytics.  
Applying to "Staff Backend Engineer" without system design evidence is inappropriate.

**Fix Needed**:
- Skill *context tags* (e.g., "Python [Analytics]" vs "Python [Web Dev]")
- Requirement matching checks context overlap

---

## Recommendations

### Priority 1: Add Opportunity Filtering

Implement `should_skip_opportunity()` function:
```python
def should_skip_opportunity(user_beliefs, opportunity) -> bool:
    # 1. Check seniority mismatch
    if "Staff" in opportunity.title or "Senior" in opportunity.title:
        if max_experience < 5 years:
            return True  # Skip
    
    # 2. Check domain mismatch
    required_domains = extract_domains(opportunity.requirements)
    user_domains = extract_domains(user_beliefs.keys())
    if overlap(required_domains, user_domains) < 0.3:
        return True  # Skip
    
    return False
```

### Priority 2: Refine Confidence Scoring

**Current**:
```python
# Cumulative bonuses
conf += 0.15  # Resume
conf += 0.25  # GitHub
conf += 0.15  # Stars
```

**Proposed**:
```python
# Evidence-weighted with caps
resume_conf = min(0.3, years * 0.03)  # 10 years = 0.3 max
github_conf = min(0.4, calculate_github_quality())  # Capped at 0.4
linkedin_conf = min(0.2, endorsement_count * 0.02)

final_conf = max(resume_conf, github_conf, linkedin_conf)  # Take strongest signal
```

### Priority 3: Add Experience Metadata

Extend `Belief` model:
```python
class Belief(BaseModel):
    attribute: str
    confidence: float
    context: str  # "Backend Engineering", "Data Analytics", "Academic"
    years_of_experience: float  # Derived from evidence
    production_validated: bool  # Has 10+ star project or 3+ years job?
```

---

## Test Results Summary

| Check | Result |
|-------|--------|
| Expert → Senior Role Match | ✓ PASS |
| Graduate → Senior Role Avoidance | ✗ FAIL |
| Hackathons Recognized as Accessible | ✓ PASS |

**Overall Grade: B**  
- **Strengths**: Confidence-based typing works
- **Weaknesses**: No selectivity, context-blind, experience-agnostic

---

## Next Steps

1. **Refactor `backend/brain/graph.py`**:
   - Add `_should_skip()` node before `reason_node`
   - Filter opportunities by seniority/domain

2. **Refactor `backend/brain/passport.py`**:
   - Revise confidence calculation with caps
   - Add `years_of_experience` and `context` fields

3. **Re-run evaluation**:
   - Target Selectivity > 40%
   - Target Grade: A

4. **Add new metrics**:
   - **Precision**: Of all proposed experiments, how many are good fits?
   - **Recall**: Of all good opportunities, how many did we propose?

---

## Appendix: Raw Data

### Senior Expert Passport
```
Python: 0.95 (Resume 10 years + GitHub 250 stars)
Django: 0.90 (Resume 8 years + GitHub)
PostgreSQL: 0.80 (Resume 7 years)
AWS: 0.65 (Resume 5 years)
Go: 0.40 (GitHub 80 stars)
```

### Career Switcher Passport
```
Python: 0.80 (Resume 3 years + GitHub)
JavaScript: 0.70 (Resume 1 year + GitHub)
SQL: 0.40 (Resume 5 years, but not validated by GitHub)
React: 0.30 (Resume 0.5 years)
```

### Fresh Graduate Passport
```
Python: 1.00 (Resume 2 years + GitHub 5 stars → hit max!)
JavaScript: 0.40 (GitHub)
Java: 0.30 (Resume)
React: 0.30 (Resume)
```

**Note**: Fresh grad Python confidence of 1.00 is the smoking gun.
