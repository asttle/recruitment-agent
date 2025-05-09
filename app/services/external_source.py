from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import aiohttp
import asyncio
import os

from app.models.candidate import Candidate
from app.services.candidate_service import candidate_service
from app.core.config import settings


class ExternalSourceService:
    async def search_candidates(self, db: Session, job_id: int, sources: List[str]) -> Dict[str, Any]:
        """
        Search for candidates from external sources based on job requirements
        """
        # Get the job details
        job = candidate_service.get_job(db, id=job_id)
        if not job:
            return {"error": "Job not found"}
        
        # Initialize results dict
        results = {
            "job_id": job_id,
            "sources": {},
            "total_candidates_found": 0
        }
        
        # Execute searches in parallel
        tasks = []
        for source in sources:
            if source == "linkedin":
                tasks.append(self._search_linkedin(job))
            elif source == "cvlibrary":
                tasks.append(self._search_cvlibrary(job))
            elif source == "naukri":
                tasks.append(self._search_naukri(job))
        
        # Wait for all search tasks to complete
        search_results = await asyncio.gather(*tasks)
        
        # Process results and add candidates to database
        for i, source in enumerate(sources):
            source_candidates = search_results[i]
            results["sources"][source] = {
                "count": len(source_candidates),
                "candidates": []
            }
            
            # Add each candidate to database if they don't exist
            for candidate_data in source_candidates:
                try:
                    # Check if candidate with this email already exists
                    existing_candidate = candidate_service.get_by_email(db, email=candidate_data["email"])
                    
                    if existing_candidate:
                        # Update existing candidate
                        for key, value in candidate_data.items():
                            if key != "email" and value:  # Don't update email and only update non-empty fields
                                setattr(existing_candidate, key, value)
                        
                        # Set the source if it's not already included
                        if existing_candidate.source != source and source not in existing_candidate.source:
                            existing_candidate.source = f"{existing_candidate.source},{source}"
                        
                        db.add(existing_candidate)
                        candidate = existing_candidate
                    else:
                        # Create new candidate
                        candidate_data["source"] = source
                        candidate = Candidate(**candidate_data)
                        db.add(candidate)
                    
                    db.commit()
                    db.refresh(candidate)
                    
                    # Create job application
                    candidate_service.match_candidates_to_job(db, job_id=job_id)
                    
                    # Add to results
                    results["sources"][source]["candidates"].append({
                        "id": candidate.id,
                        "name": f"{candidate.first_name} {candidate.last_name}",
                        "email": candidate.email
                    })
                
                except Exception as e:
                    print(f"Error adding candidate from {source}: {str(e)}")
            
            results["total_candidates_found"] += len(source_candidates)
        
        return results
    
    async def _search_linkedin(self, job) -> List[Dict[str, Any]]:
        """
        Search for candidates on LinkedIn
        """
        if not settings.LINKEDIN_API_KEY:
            return []
        
        # Extract keywords from job requirements
        keywords = self._extract_job_keywords(job.requirements)
        
        # In a real implementation, this would call the LinkedIn API
        # This is a placeholder that returns mock data
        await asyncio.sleep(1)  # Simulate API delay
        
        # Return mock candidate data
        return [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john.doe@example.com",
                "current_position": "Senior Software Engineer",
                "current_company": "Tech Inc",
                "experience_years": 5.5,
                "education": "MS Computer Science, Stanford University"
            },
            {
                "first_name": "Jane",
                "last_name": "Smith",
                "email": "jane.smith@example.com",
                "current_position": "Software Developer",
                "current_company": "Innovation Labs",
                "experience_years": 3.0,
                "education": "BS Computer Science, MIT"
            }
        ]
    
    async def _search_cvlibrary(self, job) -> List[Dict[str, Any]]:
        """
        Search for candidates on CVLibrary
        """
        if not settings.CVLIBRARY_API_KEY:
            return []
        
        # Extract keywords from job requirements
        keywords = self._extract_job_keywords(job.requirements)
        
        # In a real implementation, this would call the CVLibrary API
        # This is a placeholder that returns mock data
        await asyncio.sleep(1)  # Simulate API delay
        
        # Return mock candidate data
        return [
            {
                "first_name": "Michael",
                "last_name": "Johnson",
                "email": "michael.johnson@example.com",
                "current_position": "Full Stack Developer",
                "current_company": "WebSolutions",
                "experience_years": 4.0,
                "education": "BS Software Engineering, University of London"
            }
        ]
    
    async def _search_naukri(self, job) -> List[Dict[str, Any]]:
        """
        Search for candidates on Naukri
        """
        if not settings.NAUKRI_API_KEY:
            return []
        
        # Extract keywords from job requirements
        keywords = self._extract_job_keywords(job.requirements)
        
        # In a real implementation, this would call the Naukri API
        # This is a placeholder that returns mock data
        await asyncio.sleep(1)  # Simulate API delay
        
        # Return mock candidate data
        return [
            {
                "first_name": "Priya",
                "last_name": "Patel",
                "email": "priya.patel@example.com",
                "current_position": "Backend Developer",
                "current_company": "TechSolutions India",
                "experience_years": 3.5,
                "education": "BTech Computer Science, IIT Delhi"
            },
            {
                "first_name": "Rajesh",
                "last_name": "Kumar",
                "email": "rajesh.kumar@example.com",
                "current_position": "Senior Developer",
                "current_company": "GlobalTech",
                "experience_years": 6.0,
                "education": "MTech Computer Engineering, IIT Bombay"
            }
        ]
    
    def _extract_job_keywords(self, requirements: str) -> List[str]:
        """
        Extract keywords from job requirements for searching
        """
        # In a real implementation, this would use NLP to extract relevant keywords
        # For now, just split by commas or spaces and filter out common words
        common_words = {"and", "or", "the", "a", "an", "in", "of", "to", "for", "with", "on", "at"}
        words = []
        
        # First try splitting by commas
        if "," in requirements:
            words = [word.strip().lower() for word in requirements.split(",")]
        else:
            # Otherwise split by spaces
            words = [word.strip().lower() for word in requirements.split()]
        
        # Filter out common words and short words
        keywords = [word for word in words if word not in common_words and len(word) > 3]
        
        return keywords[:10]  # Return top 10 keywords


external_source = ExternalSourceService() 