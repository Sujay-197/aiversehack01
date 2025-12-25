"""
Skill Gap Analyzer - Identifies learning opportunities
"""
from typing import Dict, List, Tuple
from backend.llm.client import LLMClient
from backend.models import BeliefState, Opportunity

class SkillGapAnalyzer:
    """
    Analyzes skill gaps and suggests learning resources
    """
    
    LEARNING_RESOURCES = {
        # Frameworks & Languages
        "React": {
            "roadmap": "https://roadmap.sh/react",
            "youtube": "https://www.youtube.com/watch?v=Ke90Tje7VS0",
            "priority": "high"
        },
        "Python": {
            "roadmap": "https://roadmap.sh/python",
            "youtube": "https://www.youtube.com/watch?v=rfscVS0vtbw",
            "priority": "high"
        },
        "JavaScript": {
            "roadmap": "https://roadmap.sh/javascript",
            "youtube": "https://www.youtube.com/watch?v=W6NZfCO5SIk",
            "priority": "high"
        },
        "TypeScript": {
            "roadmap": "https://roadmap.sh/typescript",
            "youtube": "https://www.youtube.com/watch?v=d56mG7DezGs",
            "priority": "medium"
        },
        "Node.js": {
            "road map": "https://roadmap.sh/nodejs",
            "youtube": "https://www.youtube.com/watch?v=TlB_eWDSMt4",
            "priority": "medium"
        },
        
        # Cloud & DevOps
        "AWS": {
            "roadmap": "https://roadmap.sh/aws",
            "youtube": "https://www.youtube.com/watch?v=SOTamWNgDKc",
            "priority": "high"
        },
        "Docker": {
            "roadmap": "https://roadmap.sh/docker",
            "youtube": "https://www.youtube.com/watch?v=pTFZFxd4hOI",
            "priority": "medium"
        },
        "Kubernetes": {
            "roadmap": "https://roadmap.sh/kubernetes",
            "youtube": "https://www.youtube.com/watch?v=X48VuDVv0do",
            "priority": "medium"
        },
        
        # Databases
        "PostgreSQL": {
            "roadmap": "https://roadmap.sh/postgresql-dba",
            "youtube": "https://www.youtube.com/watch?v=qw--VYLpxG4",
            "priority": "medium"
        },
        "MongoDB": {
            "roadmap": "https://roadmap.sh/mongodb",
            "youtube": "https://www.youtube.com/watch?v=-bt_y4Loofg",
            "priority": "low"
        },
        
        # General Skills
        "System Design": {
            "roadmap": "https://roadmap.sh/system-design",
            "youtube": "https://www.youtube.com/watch?v=UzLMhqg3_Wc",
            "priority": "high"
        },
        "API Design": {
            "roadmap": "https://roadmap.sh/api-design",
            "youtube": "https://www.youtube.com/watch?v=_YlYuNMTCc8",
            "priority": "medium"
        }
    }
    
    def __init__(self):
        self.llm = LLMClient()
    
    def analyze(
        self, 
        passport: BeliefState, 
        market_opportunities: List[Opportunity]
    ) -> Dict:
        """
        Analyze skill gaps from market demand
        
        Args:
            passport: User's current belief state
            market_opportunities: Recent job opportunities
            
        Returns:
            Dict with gaps, recommendations, and learning resources
        """
        # Extract market skills
        market_skills = {}
        for opp in market_opportunities:
            for req in opp.requirements:
                market_skills[req] = market_skills.get(req, 0) + 1
        
        # Rank by frequency
        top_skills = sorted(market_skills.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Identify gaps
        user_skills = set(passport.beliefs.keys())
        gaps = [(skill, count) for skill, count in top_skills if skill not in user_skills]
        
        # LLM analysis
        prompt = f"""
You are a career advisor analyzing skill gaps.

User Current Skills: {list(user_skills)}

Market Demand (from {len(market_opportunities)} jobs):
{chr(10).join([f"- {skill}: {count} mentions" for skill, count in top_skills])}

Skill Gaps: {[skill for skill, _ in gaps]}

Provide analysis:
1. Top 3 priority skills to learn (highest ROI)
2. Estimated learning time for each (hours)
3. Why each skill matters
4. Learning order (which to learn first)

Return JSON:
{{
  "priorities": [
    {{
      "skill": "AWS",
      "mentions": 15,
      "learning_hours": 40,
      "roi": "Appears in 60% of backend roles",
      "order": 1
    }}
  ],
  "summary": "One sentence recommendation"
}}
"""
        
        response = self.llm.generate(prompt, json_response=True)
        analysis = self.llm.parse_json_response(response)
        
        # Attach learning resources
        for priority in analysis.get("priorities", []):
            skill = priority["skill"]
            if skill in self.LEARNING_RESOURCES:
                priority["resources"] = self.LEARNING_RESOURCES[skill]
            else:
                # Generic fallback
                priority["resources"] = {
                    "roadmap": f"https://roadmap.sh/search?q={skill.replace(' ', '+')}",
                    "youtube": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial",
                    "priority": "unknown"
                }
        
        return {
            "analysis": analysis,
            "market_skills": dict(top_skills),
            "gaps": gaps
        }
