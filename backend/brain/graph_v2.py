from typing import TypedDict, List, Optional
from uuid import UUID
from langgraph.graph import StateGraph, END
from backend.models import Opportunity, Belief, Experiment, BeliefState
from backend.vector_store import VectorStore

# 1. Define State
class AgentState(TypedDict):
    user_id: UUID
    opportunity: Opportunity
    belief_state: BeliefState 
    relevant_beliefs: List[Belief]
    proposed_experiment: Optional[Experiment]
    _filtered: Optional[bool]  # NEW: Track if opportunity was filtered out

# 2. Define Nodes

def retrieve_node(state: AgentState):
    """Look at the Opportunity requirements and 'recall' relevant beliefs."""
    opp = state["opportunity"]
    bs = state["belief_state"]
    print(f"\n[Node: Retrieve] Analyzing Opportunity: {opp.title}")
    
    store = VectorStore(bs)
    relevant = []
    
    for req in opp.requirements:
        hits = store.search(req)
        relevant.extend(hits)
        
    unique_beliefs = {b.attribute: b for b in relevant}.values()
    state["relevant_beliefs"] = list(unique_beliefs)
    print(f"  -> Retrieved {len(state['relevant_beliefs'])} relevant beliefs.")
    return state

def filter_node(state: AgentState):
    """
    NEW: Pre-filter opportunities before reasoning.
    Skips obviously bad-fit opportunities to improve selectivity.
    """
    beliefs = state["relevant_beliefs"]
    opp = state["opportunity"]
    
    if not beliefs:
        print(f"  [Filter] SKIP: No matching beliefs found")
        state["proposed_experiment"] = None
        state["_filtered"] = True  # Mark as filtered
        return state
    
    # FILTER 1: Seniority Check
    title_lower = opp.title.lower()
    is_senior_role = any(kw in title_lower for kw in ["staff", "senior", "lead", "principal"])
    
    if is_senior_role:
        # Use work_years (professional experience) not years_of_experience (includes projects)
        max_work_years = max([b.work_years for b in beliefs])
        if max_work_years < 3:
            print(f"  [Filter] SKIP: {opp.title} (need 3+ work years, have {max_work_years:.1f})")
            state["proposed_experiment"] = None
            state["_filtered"] = True
            return state
    
    # FILTER 2: Domain Check  
    user_contexts = set([b.context for b in beliefs])
    
    # ML/AI roles require ML context
    if any(kw in title_lower for kw in ["machine learning", "ml engineer", "research engineer", "ai engineer"]):
        if "ML/AI" not in user_contexts and "Data Science" not in user_contexts:
            print(f"  [Filter] SKIP: {opp.title} (ML role, user context: {user_contexts})")
            state["proposed_experiment"] = None
            state["_filtered"] = True
            return state
    
    # FILTER 3: Overqualification Check
    is_junior_role = any(kw in title_lower for kw in ["junior", "entry", "intern"])
    max_years = max([b.years_of_experience for b in beliefs]) if beliefs else 0
    
    if is_junior_role and max_years > 5:
        print(f"  [Filter] SKIP: {opp.title} (overqualified: {max_years:.1f} years)")
        state["proposed_experiment"] = None
        state["_filtered"] = True
        return state
    
    print(f"  [Filter] PASS: {opp.title}")
    state["_filtered"] = False
    return state

def reason_node_v2(state: AgentState):
    """
    The Scientist Logic V2: 
    - Considers both confidence AND years
    - Adjusts hypothesis based on experience level
    """
    # Check if filtered out - if so, skip reasoning
    if state.get("_filtered", False):
        print("[Node: Reason] SKIPPED (filtered out)")
        return state
    
    print("[Node: Reason] Synthesizing Experiment...")
    beliefs = state["relevant_beliefs"]
    opp = state["opportunity"]
    
    if not beliefs:
        state["proposed_experiment"] = None
        return state
    
    # Calculate stats
    max_conf = max([b.confidence for b in beliefs])
    avg_years = sum([b.years_of_experience for b in beliefs]) / len(beliefs)
    max_years = max([b.years_of_experience for b in beliefs])
    
    # Check history for recent failures
    recent_failure = False
    for b in beliefs:
        if b.history and "reject" in b.history[-1].reason.lower():
            recent_failure = True
            break
    
    # DECISION LOGIC V2
    if recent_failure:
        exp_type = "learning"
        hypers = f"CAUTION: Recent failure. Testing '{beliefs[0].attribute}' cautiously (Conf: {max_conf:.2f})."
    elif max_conf > 0.7 and max_years >= 2:
        exp_type = "verification"
        hypers = f"Strong Match: {max_conf:.2f} confidence + {max_years:.1f} years experience."
    elif max_conf > 0.5 and max_years >= 1:
        exp_type = "verification"
        hypers = f"Moderate Match: {max_conf:.2f} confidence + {max_years:.1f} years experience."
    elif max_conf > 0.3:
        exp_type = "learning"
        hypers = f"Exploratory: {max_conf:.2f} confidence. Testing fit."
    else:
        exp_type = "learning"
        hypers = f"Low Confidence: {max_conf:.2f}. High-risk exploration."

    exp = Experiment(
        user_id=state["user_id"],
        opportunity_id=opp.id,
        belief_id=beliefs[0].attribute,
        type=exp_type,
        hypothesis=hypers
    )
    
    state["proposed_experiment"] = exp
    print(f"  -> Proposed {exp.type.upper()} Experiment.")
    return state

# 3. Build Graph V2
def build_graph_v2():
    """New graph with filtering step and conditional routing"""
    
    def should_reason(state: AgentState):
        """Route decision: skip reasoning if filtered"""
        if state.get("_filtered", False):
            return "end"
        return "reason"
    
    workflow = StateGraph(AgentState)
    
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("filter", filter_node)
    workflow.add_node("reason", reason_node_v2)
    
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "filter")
    
    # Conditional edge: filter -> reason OR end
    workflow.add_conditional_edges(
        "filter",
        should_reason,
        {
            "reason": "reason",
            "end": END
        }
    )
    
    workflow.add_edge("reason", END)
    
    return workflow.compile()
