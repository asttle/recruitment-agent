import openai
from typing import Dict, List, Any, Optional
import json
from app.core.config import settings


class LLMService:
    def __init__(self):
        """
        Initialize the LLM service
        """
        if settings.LLM_API_KEY:
            openai.api_key = settings.LLM_API_KEY
    
    def extract_resume_information(self, resume_text: str) -> Dict[str, Any]:
        """
        Extract structured information from resume text using LLM
        """
        prompt = f"""
        Extract the following information from this resume:
        1. Years of experience (decimal number)
        2. Education (highest degree and institution)
        3. Current position
        4. Current company
        5. List of skills (technical and soft skills)
        
        Return the information in JSON format with the following keys:
        experience_years, education, current_position, current_company, skills (as a list of strings)
        
        Resume:
        {resume_text[:4000]}  # Limit to first 4000 chars to avoid token issues
        """
        
        try:
            response = self._call_llm(prompt)
            # Parse the JSON response
            return json.loads(response)
        except Exception as e:
            # Return a default structure in case of error
            return {
                "experience_years": None,
                "education": None,
                "current_position": None,
                "current_company": None,
                "skills": []
            }
    
    def evaluate_candidate_job_match(self, candidate, job) -> Dict[str, Any]:
        """
        Evaluate how well a candidate matches a job using LLM
        Returns a match score and feedback
        """
        # Prepare candidate information
        candidate_info = f"""
        Candidate: {candidate.first_name} {candidate.last_name}
        Experience: {candidate.experience_years} years
        Education: {candidate.education}
        Current Position: {candidate.current_position}
        Current Company: {candidate.current_company}
        Skills: {', '.join(skill.name for skill in candidate.skills)}
        """
        
        # Prepare job information
        job_info = f"""
        Job Title: {job.title}
        Description: {job.description}
        Requirements: {job.requirements}
        Location: {job.location}
        Job Type: {job.job_type}
        """
        
        prompt = f"""
        Evaluate how well the candidate matches the job requirements.
        
        {candidate_info}
        
        {job_info}
        
        Rate the match on a scale from 0.0 to 1.0, where 1.0 is a perfect match.
        Provide feedback explaining why the candidate is or is not a good match.
        
        Return your evaluation in JSON format with the following keys:
        score (a decimal number between 0.0 and 1.0), feedback (a string with your analysis)
        """
        
        try:
            response = self._call_llm(prompt)
            # Parse the JSON response
            return json.loads(response)
        except Exception as e:
            # Return a default structure in case of error
            return {
                "score": 0.0,
                "feedback": f"Error evaluating candidate: {str(e)}"
            }
    
    def _call_llm(self, prompt: str) -> str:
        """
        Call the language model API with the given prompt
        """
        try:
            response = openai.ChatCompletion.create(
                model=settings.LLM_MODEL,
                messages=[
                    {"role": "system", "content": "You are a recruitment assistant that analyzes resumes and job descriptions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1  # Low temperature for more consistent results
            )
            return response.choices[0].message.content
        except Exception as e:
            # Handle the case where the API call fails
            print(f"Error calling LLM API: {str(e)}")
            return "{}"  # Return empty JSON in case of error


llm_service = LLMService() 