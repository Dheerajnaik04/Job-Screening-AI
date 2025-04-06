from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    requirements = Column(JSON)  # Structured requirements
    responsibilities = Column(JSON)  # Structured responsibilities
    skills = Column(JSON)  # Required skills
    embedding = Column(JSON)  # Job embedding vector
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    matches = relationship("Match", back_populates="job")

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True)
    cv_id = Column(String(50), unique=True, nullable=False)
    name = Column(String(255))
    email = Column(String(255))
    education = Column(JSON)  # Education history
    experience = Column(JSON)  # Work experience
    skills = Column(JSON)  # Skills and certifications
    embedding = Column(JSON)  # Candidate embedding vector
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    matches = relationship("Match", back_populates="candidate")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    match_score = Column(Float, nullable=False)
    skill_match = Column(JSON)  # Detailed skill matching
    experience_match = Column(JSON)  # Experience matching details
    status = Column(String(50), default="pending")  # pending, shortlisted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", back_populates="matches")
    candidate = relationship("Candidate", back_populates="matches")
    interviews = relationship("Interview", back_populates="match")

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    scheduled_time = Column(DateTime)
    duration = Column(Integer)  # Duration in minutes
    interview_type = Column(String(50))  # online, in-person, phone
    status = Column(String(50), default="scheduled")  # scheduled, completed, cancelled
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    match = relationship("Match", back_populates="interviews") 