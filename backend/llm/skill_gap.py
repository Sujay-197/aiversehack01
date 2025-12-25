"""
Skill Gap Analyzer - Identifies learning opportunities
"""
from typing import Dict, List, Tuple
from backend.llm.client import LLMClient
from backend.models import BeliefState, Opportunity

class SkillGapAnalyzer:
    """
    Analyzes skill gaps and suggests learning resources dynamically using LLM
    """
    
    def __init__(self):
        self.llm = LLMClient()
    
    def analyze(
        self, 
        passport: BeliefState, 
        market_opportunities: List[Opportunity]
    ) -> Dict:
        """
        Analyze skill gaps from market demand and generate curated resources
        
        Args:
            passport: User's current belief state
            market_opportunities: Recent job opportunities
            
        Returns:
            Dict with gaps, recommendations, and curated learning resources
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
        
        # LLM analysis with curated resource generation
        prompt = f"""
You are a career advisor analyzing skill gaps.

User Current Skills: {list(user_skills)}

Market Demand (from {len(market_opportunities)} jobs):
{chr(10).join([f"- {skill}: {count} mentions" for skill, count in top_skills])}

Skill Gaps: {[skill for skill, _ in gaps]}

Provide analysis and curated learning resources:
1. Identify top 3 priority skills to learn (highest ROI)
2. For each skill, provide:
   - learning_hours: Estimated time to reach basic proficiency
   - roi: Why this skill matters specifically for this market
   - roadmap: A link to a roadmap.sh (if applicable) or a high-quality learning path URL
   - youtube: A link to a specific, high-quality YouTube tutorial or playlist
   - priority: 'high', 'medium', or 'low'

Return ONLY valid JSON:
{{
  "priorities": [
    {{
      "skill": "AWS",
      "mentions": 15,
      "learning_hours": 40,
      "roi": "Appears in 60% of backend roles",
      "order": 1,
      "resources": {{
        "roadmap": "https://roadmap.sh/aws",
        "youtube": "https://www.youtube.com/watch?v=SOTamWNgDKc",
        "priority": "high"
      }}
    }}
  ],
  "summary": "One sentence recommendation"
}}
"""
        
        response = self.llm.generate(prompt, json_response=True)
        analysis = self.llm.parse_json_response(response)
        
        return {
            "analysis": analysis,
            "market_skills": dict(top_skills),
            "gaps": gaps
        }
