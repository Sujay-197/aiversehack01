"""
Unified Resume Parser
Facade that selects between RAG (higher accuracy, slower) and Direct (faster, less setup) strategies.
Implements automatic fallback logic.
"""
from typing import Optional, Literal
import uuid
from backend.models import ResumeEvidence
from backend.llm.resume_parser import ResumeParser
from backend.llm.rag_resume_parser import RAGResumeParser
import os

class UnifiedResumeParser:
    """
    Unified entry point for resume parsing.
    
    Strategies:
    - 'auto': Try RAG first, fallback to Direct on error.
    - 'rag': Use Few-Shot RAG (requires vector store).
    - 'direct': Use Zero-Shot Direct LLM.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "keyapi")
        self._rag_parser: Optional[RAGResumeParser] = None
        self._direct_parser: Optional[ResumeParser] = None
    
    @property
    def rag_parser(self) -> RAGResumeParser:
        if not self._rag_parser:
            self._rag_parser = RAGResumeParser(api_key=self.api_key)
        return self._rag_parser
    
    @property
    def direct_parser(self) -> ResumeParser:
        if not self._direct_parser:
            self._direct_parser = ResumeParser() # Uses internal client which handles its own key
        return self._direct_parser

    def parse(self, resume_text: str, user_id: uuid.UUID = None, strategy: Literal["auto", "rag", "direct"] = "auto") -> ResumeEvidence:
        """
        Parse resume using specified strategy.
        """
        if user_id is None:
            user_id = uuid.uuid4()

        if strategy == "rag":
            return self.rag_parser.parse(resume_text, user_id)
        
        elif strategy == "direct":
            return self.direct_parser.parse(resume_text, user_id)
        
        else: # strategy == "auto"
            try:
                # Try RAG first
                print("[UnifiedParser] Attempting RAG strategy...")
                result = self.rag_parser.parse(resume_text, user_id)
                # Simple validation check: did we get skills?
                if result.skills:
                    return result
                print("[UnifiedParser] RAG returned no skills, failing over to Direct...")
                raise ValueError("RAG parsing unsatisfactory")
                
            except Exception as e:
                print(f"[UnifiedParser] RAG failed/unsatisfactory ({e}). Falling back to Direct strategy...")
                return self.direct_parser.parse(resume_text, user_id)

    def add_example(self, resume_text: str, parsed_output: dict):
        """Pass-through to RAG parser to improve future performance"""
        self.rag_parser.add_example(resume_text, parsed_output)
