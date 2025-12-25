from backend.brain.graph_v2 import build_graph_v2
from backend.models import Opportunity, BeliefState, Belief
from uuid import uuid4

# Test if conditional routing works
graph = build_graph_v2()

# Create test state
user_id = uuid4()
passport = BeliefState(user_id=user_id, beliefs={
    "Python": Belief(attribute="Python", confidence=0.5, basis="test", years_of_experience=1.0, context="General")
})

opp_ml = Opportunity(
    title="ML Research Engineer",
    company="AI Lab",
    url="https://test.com",
    type="job",
    requirements=["Python", "PyTorch"],
    source="test"
)

result = graph.invoke({
    "user_id": user_id,
    "opportunity": opp_ml,
    "belief_state": passport,
    "relevant_beliefs": [],
    "proposed_experiment": None
})

print(f"\nFiltered: {result.get('_filtered', False)}")
print(f"Experiment Created: {result.get('proposed_experiment') is not None}")
