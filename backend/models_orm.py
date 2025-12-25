from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from .database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False) # Added for Auth
    full_name = Column(String, nullable=True)
    github_username = Column(String, nullable=True)
    linkedin_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    evidence = relationship("Evidence", back_populates="user")
    experiments = relationship("Experiment", back_populates="user")
    belief_state = relationship("BeliefState", uselist=False, back_populates="user")

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    type = Column(String, nullable=False) # 'resume', 'github_repo', 'linkedin_profile'
    content_raw = Column(JSON, nullable=True)
    source_url = Column(String, nullable=True)
    captured_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="evidence")

# Note: Keeping Embeddings model simplified for SQLite (no pgvector)
# We won't use this table for vector search in this iteration (using in-memory simulation)
class EvidenceEmbedding(Base):
    __tablename__ = "evidence_embeddings"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    evidence_id = Column(String, ForeignKey("evidence.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    chunk_text = Column(Text, nullable=True)
    # embedding = ... (Skipping vector type for SQLite compatibility)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BeliefState(Base):
    __tablename__ = "belief_state"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    version = Column(Integer, default=1)
    assumptions = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="belief_state")
    experiments = relationship("Experiment", back_populates="belief_state")

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    belief_state_id = Column(String, ForeignKey("belief_state.id"), nullable=True)
    type = Column(String, nullable=False)
    hypothesis = Column(Text, nullable=False)
    meta_data = Column(JSON, nullable=True)
    status = Column(String, default='pending')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="experiments")
    belief_state = relationship("BeliefState", back_populates="experiments")
    outcomes = relationship("Outcome", back_populates="experiment")

class Outcome(Base):
    __tablename__ = "outcomes"

    id = Column(String, primary_key=True, default=generate_uuid)
    experiment_id = Column(String, ForeignKey("experiments.id"), nullable=False)
    type = Column(String, nullable=False)
    raw_response = Column(Text, nullable=True)
    belief_impact = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    experiment = relationship("Experiment", back_populates="outcomes")
