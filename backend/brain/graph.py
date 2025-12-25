from typing import TypedDict, List, Optional
from uuid import UUID
from langgraph.graph import StateGraph, END
from backend.models import Opportunity, Belief, Experiment, BeliefState
from backend.vector_store import VectorStore
from backend.brain.hypothesis import HypothesisGenerator # We can reuse logic or rewrite.

# 1. Define State
class AgentState(TypedDict):
    user_id: UUID
    opportunity: Opportunity
    # The full user context (for vector search)
    belief_state: BeliefState 
    # Working memory
    relevant_beliefs: List[Belief]
    proposed_experiment: Optional[Experiment]

# 2. Define Nodes

def retrieve_node(state: AgentState):
    """
    Look at the Opportunity requirements and 'recall' relevant beliefs.
    """
    opp = state["opportunity"]
    bs = state["belief_state"]
    print(f"\n[Node: Retrieve] Analyzing Opportunity: {opp.title}")
    
    store = VectorStore(bs)
    relevant = []
    
    # For each requirement, search memory
    for req in opp.requirements:
        hits = store.search(req)
        relevant.extend(hits)
        
    # Deduplicate
    unique_beliefs = {b.attribute: b for b in relevant}.values()
    state["relevant_beliefs"] = list(unique_beliefs)
    print(f"  -> Retrieved {len(state['relevant_beliefs'])} relevant beliefs.")
    return state

def reason_node(state: AgentState):
    """
    The Scientist Logic. Compares relevant beliefs vs requirements.
    """
    print("[Node: Reason] Synthesizing Experiment...")
    beliefs = state["relevant_beliefs"]
    opp = state["opportunity"]
    
    # We can reuse the HypothesisGenerator logic but applied to this subset
    # Or implement a lighter version here.
    
    # Simplified Logic for Graph Demo:
    # 1. Check coverage
    reqs = set(r.lower() for r in opp.requirements)
    
    # Extract known capabilities from retrieved beliefs + their ontology expansions
    known_capabilities = set()
    ontology = VectorStore.SKILL_ONTOLOGY
    
    matched_beliefs = []
    
    for b in beliefs:
        matched_beliefs.append(b)
        attr = b.attribute
        known_capabilities.add(attr.lower())
        # Add implied skills
        for term in ontology.get(attr, []):
            known_capabilities.add(term.lower())
            
    # Check match
    missing = []
    for r in reqs:
        if r not in known_capabilities:
            missing.append(r)
            
    # Decide
    max_conf = max([b.confidence for b in matched_beliefs]) if matched_beliefs else 0.0
    
    # Check history for recent failures
    recent_failure = False
    for b in matched_beliefs:
        print(f"DEBUG: Checking history for {b.attribute}: {len(b.history)} entries")
        if b.history:
            print(f"DEBUG: Last entry: {b.history[-1].reason}")
        
        if b.history and "reject" in b.history[-1].reason.lower():
            recent_failure = True
            break
    
    if recent_failure:
        exp_type = "learning" # Downgrade to learning even if high confidence
        hypers = f"CAUTION: Recent failure detected. Testing '{matched_beliefs[0].attribute}' cautiously (Conf: {max_conf:.2f})."
    elif max_conf > 0.6:
        exp_type = "verification"
        hypers = f"Graph Logic: High Confidence ({max_conf:.2f}) in {len(matched_beliefs)} skills."
    else:
        exp_type = "learning"
        hypers = f"Graph Logic: Low Confidence ({max_conf:.2f}). Testing fit."

    # Create Experiment
    exp = Experiment(
        user_id=state["user_id"],
        opportunity_id=opp.id,
        belief_id=matched_beliefs[0].attribute if matched_beliefs else "None",
        type=exp_type,
        hypothesis=hypers
    )
    
    state["proposed_experiment"] = exp
    print(f"  -> Proposed {exp.type.upper()} Experiment.")
    return state

# 3. Build Graph
def build_graph():
    workflow = StateGraph(AgentState)
    
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("reason", reason_node)
    
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "reason")
    workflow.add_edge("reason", END)
    
    return workflow.compile()
