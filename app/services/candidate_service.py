from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from fastapi import HTTPException

from app.models.candidate import Candidate, Job, JobApplication, Skill
from app.models.base import CRUDBase
from app.api.schemas import CandidateCreate, CandidateUpdate, JobCreate, JobUpdate
from app.services.llm_service import llm_service


class CandidateService(CRUDBase):
    def get_candidates(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        source: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Candidate]:
        """
        Get candidates with optional filters
        """
        query = db.query(self.model)
        
        if source:
            query = query.filter(self.model.source == source)
        
        if status:
            query = query.filter(self.model.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def get_by_email(self, db: Session, *, email: str) -> Optional[Candidate]:
        """
        Get a candidate by email
        """
        return db.query(self.model).filter(self.model.email == email).first()
    
    def update_status(self, db: Session, *, candidate_id: int, status: str) -> Candidate:
        """
        Update candidate status
        """
        candidate = self.get(db, id=candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        candidate.status = status
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        return candidate
    
    def create_job(self, db: Session, *, obj_in: JobCreate) -> Job:
        """
        Create a new job
        """
        job = Job(
            title=obj_in.title,
            description=obj_in.description,
            requirements=obj_in.requirements,
            location=obj_in.location,
            job_type=obj_in.job_type
        )
        
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    
    def get_job(self, db: Session, *, id: int) -> Optional[Job]:
        """
        Get a job by ID
        """
        return db.query(Job).filter(Job.id == id).first()
    
    def update_job(self, db: Session, *, job_id: int, job_in: JobUpdate) -> Job:
        """
        Update job details
        """
        job = self.get_job(db, id=job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Update attributes
        for field, value in job_in.dict(exclude_unset=True).items():
            setattr(job, field, value)
        
        db.add(job)
        db.commit()
        db.refresh(job)
        return job
    
    def match_candidates_to_job(self, db: Session, *, job_id: int) -> List[Candidate]:
        """
        Match existing candidates to a job based on skills and requirements
        Uses LLM to score candidates
        """
        job = self.get_job(db, id=job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        
        # Get all candidates
        candidates = db.query(Candidate).all()
        matched_candidates = []
        
        for candidate in candidates:
            # Use LLM to determine match score and feedback
            match_result = llm_service.evaluate_candidate_job_match(candidate, job)
            
            # Update candidate with match score
            candidate.match_score = match_result["score"]
            candidate.llm_feedback = match_result["feedback"]
            db.add(candidate)
            
            # Create job application if score is above threshold (e.g., 0.7)
            if match_result["score"] >= 0.7:
                job_application = JobApplication(
                    candidate_id=candidate.id,
                    job_id=job.id,
                    status="matched"
                )
                db.add(job_application)
                matched_candidates.append(candidate)
        
        db.commit()
        return matched_candidates
    
    def add_skill(self, db: Session, *, candidate_id: int, skill_name: str, category: Optional[str] = None) -> Skill:
        """
        Add a skill to a candidate
        """
        candidate = self.get(db, id=candidate_id)
        if not candidate:
            raise HTTPException(status_code=404, detail="Candidate not found")
        
        # Check if skill already exists
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if not skill:
            skill = Skill(name=skill_name, category=category)
            db.add(skill)
            db.commit()
            db.refresh(skill)
        
        # Add skill to candidate if not already added
        if skill not in candidate.skills:
            candidate.skills.append(skill)
            db.add(candidate)
            db.commit()
            db.refresh(candidate)
        
        return skill


candidate_service = CandidateService(Candidate) 