"""
Central Configuration for Career Scientist Agent
"""
import os
from dataclasses import dataclass

@dataclass
class Thresholds:
    # Passport / Beliefs
    RESUME_CONFIDENCE_CAP: float = 0.45
    GITHUB_CONFIDENCE_CAP: float = 0.35
    MAX_CONFIDENCE_CAP: float = 1.0
    
    # Hypothesis / Experiments
    VERIFICATION_CONFIDENCE_THRESHOLD: float = 0.7  # Above this, we verify strength
    LEARNING_MIN_CONFIDENCE: float = 0.1  # Below this, it's just learning
    
    # Market Filtering
    MIN_SENIORITY_YEARS: float = 3.0  # For senior roles

@dataclass
class LLMConfig:
    MODEL_NAME: str = "gemini-2.0-flash-exp"
    EMBEDDING_MODEL: str = "models/embedding-001"
    TEMPERATURE_DETERMINISTIC: float = 0.0
    TEMPERATURE_CREATIVE: float = 0.7

class Config:
    THRESHOLDS = Thresholds()
    LLM = LLMConfig()
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    RAG_EXAMPLES_PATH = os.path.join(DATA_DIR, "resume_examples.json")

# Global instance
config = Config()
