from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.schemas import CandidateCreate, CandidateResponse, JobCreate, JobResponse
from app.services.candidate_service import candidate_service
from app.services.resume_parser import resume_parser
from app.services.external_source import external_source
from app.services.email_service import email_service
from app.core.deps import get_db

router = APIRouter()


@router.post("/candidates/", response_model=CandidateResponse)
async def create_candidate(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    *,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    resume: UploadFile = File(...)
):
    """
    Create a new candidate with uploaded resume
    """
    # Save the resume file
    resume_path = await resume_parser.save_resume(resume)
    
    # Create candidate with basic info
    candidate_in = CandidateCreate(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        resume_path=resume_path,
        source="applied"
    )
    
    # Create the candidate in DB
    candidate = candidate_service.create(db, obj_in=candidate_in)
    
    # Process resume in background
    background_tasks.add_task(
        resume_parser.process_resume,
        db=db,
        candidate_id=candidate.id,
        resume_path=resume_path
    )
    
    return candidate


@router.get("/candidates/", response_model=List[CandidateResponse])
def get_candidates(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    source: Optional[str] = None,
    status: Optional[str] = None
):
    """
    Get list of candidates with optional filtering
    """
    return candidate_service.get_candidates(
        db=db, 
        skip=skip, 
        limit=limit,
        source=source,
        status=status
    )


@router.post("/jobs/", response_model=JobResponse)
def create_job(
    job_in: JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Create a new job posting and find matching candidates
    """
    # Create the job
    job = candidate_service.create_job(db, obj_in=job_in)
    
    # Find matching candidates in background
    background_tasks.add_task(
        candidate_service.match_candidates_to_job,
        db=db,
        job_id=job.id
    )
    
    return job


@router.post("/search/external/")
async def search_external_candidates(
    job_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    sources: List[str] = ["linkedin", "cvlibrary", "naukri"]
):
    """
    Search for candidates from external sources like LinkedIn, CVLibrary, Naukri
    """
    # Get the job details
    job = candidate_service.get_job(db, id=job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Search for candidates in background
    background_tasks.add_task(
        external_source.search_candidates,
        db=db,
        job_id=job_id,
        sources=sources
    )
    
    return {"message": "External candidate search initiated", "job_id": job_id}


@router.post("/candidates/{candidate_id}/contact")
async def contact_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    job_id: Optional[int] = None
):
    """
    Send an email to contact the candidate for interview
    """
    # Get the candidate
    candidate = candidate_service.get(db, id=candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Get the job if provided
    job = None
    if job_id:
        job = candidate_service.get_job(db, id=job_id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
    
    # Send the email
    sent = await email_service.send_interview_invitation(candidate, job)
    
    if sent:
        # Update candidate status
        candidate_service.update_status(db, candidate_id=candidate_id, status="contacted")
        return {"message": "Email sent successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to send email")


@router.post("/candidates/{candidate_id}/schedule")
async def schedule_interview(
    candidate_id: int,
    db: Session = Depends(get_db),
    job_id: Optional[int] = None,
    date_time: str = Form(...)
):
    """
    Schedule an interview with a candidate
    """
    # Get the candidate
    candidate = candidate_service.get(db, id=candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    
    # Schedule the interview
    scheduled = await email_service.schedule_interview(candidate, date_time, job_id)
    
    if scheduled:
        # Update candidate status
        candidate_service.update_status(db, candidate_id=candidate_id, status="interview_scheduled")
        return {"message": "Interview scheduled successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to schedule interview")
