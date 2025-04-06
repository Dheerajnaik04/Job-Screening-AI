from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    required_skills = Column(JSON, nullable=False)
    preferred_skills = Column(JSON, nullable=False)
    experience = Column(String, nullable=False)
    education = Column(String, nullable=False)
    responsibilities = Column(JSON, nullable=False)
    embedding = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    matches = relationship("Match", back_populates="job")

class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String)
    skills = Column(JSON, nullable=False)
    experience = Column(JSON, nullable=False)
    education = Column(JSON, nullable=False)
    embedding = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    matches = relationship("Match", back_populates="candidate")

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id"), nullable=False)
    match_score = Column(Float, nullable=False)
    match_details = Column(JSON, nullable=False)
    status = Column(String, nullable=False)  # pending, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", back_populates="matches")
    candidate = relationship("Candidate", back_populates="matches")
    interview = relationship("Interview", back_populates="match", uselist=False)

class Interview(Base):
    __tablename__ = "interviews"
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)  # in minutes
    type = Column(String, nullable=False)
    format = Column(String, nullable=False)
    topics = Column(JSON, nullable=False)
    interviewers = Column(JSON, nullable=False)
    status = Column(String, nullable=False)  # scheduled, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    match = relationship("Match", back_populates="interview") 