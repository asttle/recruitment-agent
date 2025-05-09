import os
import shutil
from fastapi import UploadFile
from pathlib import Path
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session

from app.core.config import settings
from app.services.candidate_service import candidate_service
from app.services.llm_service import llm_service


class ResumeParser:
    async def save_resume(self, resume: UploadFile) -> str:
        """
        Save uploaded resume to disk
        """
        # Create upload directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(resume.filename)[1]
        unique_filename = f"{resume.filename.split('.')[0]}_{os.urandom(8).hex()}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(resume.file, buffer)
        
        return file_path
    
    async def process_resume(self, db: Session, candidate_id: int, resume_path: str) -> Dict[str, Any]:
        """
        Extract information from resume using LLM and update candidate
        """
        candidate = candidate_service.get(db, id=candidate_id)
        if not candidate:
            return {"error": "Candidate not found"}
        
        # Extract text from resume
        resume_text = await self._extract_text_from_file(resume_path)
        
        # Use LLM to extract information
        resume_data = llm_service.extract_resume_information(resume_text)
        
        # Update candidate with extracted information
        update_data = {
            "experience_years": resume_data.get("experience_years"),
            "education": resume_data.get("education"),
            "current_position": resume_data.get("current_position"),
            "current_company": resume_data.get("current_company"),
        }
        
        # Update candidate in database
        for key, value in update_data.items():
            if value:
                setattr(candidate, key, value)
        
        db.add(candidate)
        db.commit()
        db.refresh(candidate)
        
        # Add skills
        if "skills" in resume_data and resume_data["skills"]:
            for skill in resume_data["skills"]:
                candidate_service.add_skill(db, candidate_id=candidate.id, skill_name=skill)
        
        return resume_data
    
    async def _extract_text_from_file(self, file_path: str) -> str:
        """
        Extract text from PDF or DOCX file
        """
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == ".pdf":
            return await self._extract_text_from_pdf(file_path)
        elif file_extension == ".docx":
            return await self._extract_text_from_docx(file_path)
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
    
    async def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF file
        """
        try:
            # Using PyPDF2 (you would need to install this library)
            from PyPDF2 import PdfReader
            
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            return text
        except Exception as e:
            # Fallback to LLM if PDF extraction fails
            return f"Error extracting PDF: {str(e)}"
    
    async def _extract_text_from_docx(self, docx_path: str) -> str:
        """
        Extract text from DOCX file
        """
        try:
            # Using python-docx (you would need to install this library)
            import docx
            
            doc = docx.Document(docx_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            return text
        except Exception as e:
            # Fallback to LLM if DOCX extraction fails
            return f"Error extracting DOCX: {str(e)}"


resume_parser = ResumeParser()
