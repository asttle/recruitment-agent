from pydantic import BaseModel, EmailStr, HttpUrl, constr, validator, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None


class SkillCreate(SkillBase):
    pass


class SkillResponse(SkillBase):
    id: int
    
    class Config:
        orm_mode = True


class CandidateBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    resume_path: Optional[str] = None
    source: str = "applied"  # "applied", "linkedin", "cvlibrary", "naukri", etc.


class CandidateCreate(CandidateBase):
    pass


class CandidateUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    experience_years: Optional[float] = None
    education: Optional[str] = None
    current_position: Optional[str] = None
    current_company: Optional[str] = None
    match_score: Optional[float] = None
    llm_feedback: Optional[str] = None
    status: Optional[str] = None


class CandidateResponse(CandidateBase):
    id: int
    experience_years: Optional[float] = None
    education: Optional[str] = None
    current_position: Optional[str] = None
    current_company: Optional[str] = None
    match_score: Optional[float] = 0.0
    llm_feedback: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    status: str
    skills: List[SkillResponse] = []
    
    class Config:
        orm_mode = True


class JobBase(BaseModel):
    title: str
    description: str
    requirements: str
    location: Optional[str] = None
    job_type: str


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None


class JobResponse(JobBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True


class JobApplicationBase(BaseModel):
    candidate_id: int
    job_id: int
    status: str = "applied"


class JobApplicationCreate(JobApplicationBase):
    pass


class JobApplicationUpdate(BaseModel):
    status: Optional[str] = None
    email_sent: Optional[bool] = None
    response_received: Optional[bool] = None


class JobApplicationResponse(JobApplicationBase):
    id: int
    applied_date: datetime
    last_updated: Optional[datetime] = None
    email_sent: bool
    response_received: bool
    
    class Config:
        orm_mode = True


class CandidateSearchParams(BaseModel):
    job_id: int
    sources: List[str] = ["linkedin", "cvlibrary", "naukri"]
    max_candidates: int = 50


class EmailTemplateParams(BaseModel):
    template_name: str = "interview_invitation"
    subject: Optional[str] = None
    custom_message: Optional[str] = None
