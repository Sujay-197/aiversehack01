from typing import List, Optional, Dict, Any
from uuid import UUID
import uuid
from datetime import datetime
from pydantic import BaseModel, HttpUrl, Field

# --- Shared Models ---

class Skill(BaseModel):
    name: str
    category: Optional[str] = None # e.g., "Language", "Framework"
    years_of_experience: Optional[float] = None

class DateRange(BaseModel):
    start_date: Optional[str] = None # ISO format or "YYYY-MM"
    end_date: Optional[str] = None   # "Present" or ISO format

# --- Evidence Models ---

class BaseEvidence(BaseModel):
    user_id: UUID
    captured_at: datetime = Field(default_factory=datetime.now)
    source_url: Optional[str] = None

class ResumeEvidence(BaseEvidence):
    evidence_type: str = "resume"
    full_name: str
    email: Optional[str] = None
    summary: Optional[str] = None
    skills: List[Skill] = []
    work_experience: List[Dict[str, Any]] = [] # Flexible for now
    education: List[Dict[str, Any]] = []

class GitHubRepo(BaseModel):
    name: str
    url: str
    description: Optional[str] = None
    primary_language: Optional[str] = None
    stars: int = 0
    updated_at: Optional[str] = None

class GitHubEvidence(BaseEvidence):
    evidence_type: str = "github"
    username: str
    bio: Optional[str] = None
    public_repos: int = 0
    top_repositories: List[GitHubRepo] = []
    followers: int = 0

class LinkedInEvidence(BaseEvidence):
    evidence_type: str = "linkedin"
    profile_url: str
    headline: Optional[str] = None
    about: Optional[str] = None
    experience: List[Dict[str, Any]] = [] # Raw text or structured
    skills: List[str] = []

# --- Database / DTO Models ---

class User(BaseModel):
    id: Optional[UUID] = None
    email: str
    full_name: Optional[str] = None
    github_username: Optional[str] = None
    linkedin_url: Optional[str] = None

# --- Belief Engine Models (The Failure Passport) ---

class BeliefUpdate(BaseModel):
    timestamp: datetime = Field(default_factory=datetime.now)
    old_confidence: float
    new_confidence: float
    reason: str # "Verified via GitHub repo analysis", "Failed interview"

class Belief(BaseModel):
    attribute: str # "Python", "System Design", "Leadership"
    confidence: float = Field(0.0, ge=0.0, le=1.0) # 0.0 to 1.0
    basis: str # Primary reason for current belief
    evidence_ids: List[UUID] = [] # Pointers to raw evidence
    history: List[BeliefUpdate] = []
    years_of_experience: float = 0.0  # Total skill practice (resume + projects)
    work_years: float = 0.0  # NEW: Professional work experience only (from resume)
    context: str = "General"  # "Backend Engineering", "Data Analytics", etc.

class BeliefState(BaseModel):
    user_id: UUID
    version: int = 1
    # Key is the attribute name (e.g. "Python") for easy lookup
    beliefs: Dict[str, Belief] = {}
    generated_at: datetime = Field(default_factory=datetime.now)

# --- Market Models (The Tests) ---

class Opportunity(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    title: str
    company: str
    url: str
    description: Optional[str] = None
    type: str # "internship", "job", "hackathon"
    requirements: List[str] = [] # "Python", "React", "3 years exp"
    # Metadata for the hypothesis engine
    posted_date: Optional[str] = None
    source: str = "simulated"

# --- Experiment Models (The Hypothesis) ---

class Experiment(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    user_id: UUID
    # The outcome we are trying to verify or learn
    belief_id: Optional[str] = None # Linking to Attribute name for now (e.g. "Python")
    opportunity_id: UUID
    
    type: str # "verification" (High Confidence), "learning" (Low Confidence), "discovery" (No Confidence)
    hypothesis: str # "If I apply, I will get an interview because my conf is 0.9"
    status: str = "proposed" # proposed, active, completed
    created_at: datetime = Field(default_factory=datetime.now)

# --- Outcome Models (The feedback) ---

class Outcome(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    experiment_id: UUID
    result: str # "rejection", "interview", "ghosted", "offer"
    feedback: Optional[str] = None # "Not enough experience in X"
    created_at: datetime = Field(default_factory=datetime.now)
