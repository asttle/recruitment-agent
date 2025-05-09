from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base


# Association table for candidate skills
candidate_skills = Table(
    'candidate_skills',
    Base.metadata,
    Column('candidate_id', Integer, ForeignKey('candidates.id')),
    Column('skill_id', Integer, ForeignKey('skills.id'))
)


class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    category = Column(String(50), nullable=True)
    
    # Relationships
    candidates = relationship("Candidate", secondary=candidate_skills, back_populates="skills")


class Candidate(Base):
    __tablename__ = "candidates"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20), nullable=True)
    resume_path = Column(String(255), nullable=True)
    source = Column(String(50))  # "applied", "linkedin", "cvlibrary", "naukri", etc.
    
    # Resume extracted data
    experience_years = Column(Float, nullable=True)
    education = Column(Text, nullable=True)
    current_position = Column(String(255), nullable=True)
    current_company = Column(String(255), nullable=True)
    
    # Match scores
    match_score = Column(Float, default=0.0)
    llm_feedback = Column(Text, nullable=True)
    
    # Tracking
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Status
    status = Column(String(50), default="new")  # new, contacted, interview_scheduled, rejected, hired
    
    # Relationships
    skills = relationship("Skill", secondary=candidate_skills, back_populates="candidates")
    jobs = relationship("JobApplication", back_populates="candidate")


class JobApplication(Base):
    __tablename__ = "job_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    
    # Application data
    status = Column(String(50), default="applied")  # applied, screening, interview, offer, rejected, accepted
    applied_date = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Email communication
    email_sent = Column(Boolean, default=False)
    response_received = Column(Boolean, default=False)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="jobs")
    job = relationship("Job", back_populates="candidates")


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(Text)
    requirements = Column(Text)
    location = Column(String(255), nullable=True)
    job_type = Column(String(50))  # full-time, part-time, contract
    
    # Dates
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    candidates = relationship("JobApplication", back_populates="job")
