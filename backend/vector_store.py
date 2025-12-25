from typing import List, Dict, Any
from backend.models import BeliefState, Belief

class VectorStore:
    """
    Simulates a Vector Database (pgvector/Qdrant).
    In reality, we would embed the query and search for nearest neighbor Beliefs.
    Here, we simulate "Semantic Search" using our Skill Ontology.
    """
    
    # Shared Ontology (simulating valid vector space relationships)
    SKILL_ONTOLOGY = {
        "PostgreSQL": ["SQL", "Database", "RDBMS", "Backend"],
        "Python": ["Django", "Flask", "FastAPI", "Scripting", "Backend", "AI", "LLM"],
        "React": ["JavaScript", "Frontend", "UI", "Web"],
        "JavaScript": ["React", "Vue", "Node", "Frontend", "Web"],
        "Git": ["Version Control", "GitHub", "GitLab", "DevOps"]
    }

    def __init__(self, belief_state: BeliefState):
        self.belief_state = belief_state

    def search(self, query: str, limit: int = 5) -> List[Belief]:
        """
        Simulate vector search: "Find beliefs relevant to 'query'".
        E.g. query="Database" -> returns Belief("PostgreSQL") if user has it.
        """
        print(f"  [VectorStore] Semantic Search for: '{query}'...")
        hits = []
        query_lower = query.lower()
        
        for attr, belief in self.belief_state.beliefs.items():
            # 1. Exact Match (High Score)
            if query_lower in attr.lower() or attr.lower() in query_lower:
                hits.append(belief)
                continue
            
            # 2. Semantic Match (Simulated via Ontology)
            # If the Belief (e.g. Postgres) relates to the Query (e.g. Database)
            related_terms = self.SKILL_ONTOLOGY.get(attr, [])
            if any(term.lower() == query_lower for term in related_terms):
                print(f"    -> Found Semantic Match: '{attr}' implies '{query}'")
                hits.append(belief)
        
        return hits[:limit]
