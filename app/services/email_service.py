import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
import aiosmtplib
from datetime import datetime

from app.core.config import settings


class EmailService:
    async def send_interview_invitation(self, candidate, job=None) -> bool:
        """
        Send interview invitation email to candidate
        """
        subject = f"Interview Invitation - {job.title if job else 'Our Company'}"
        
        # Construct the email body
        body = f"""
        Dear {candidate.first_name} {candidate.last_name},
        
        Thank you for your interest in {job.title if job else 'our company'}.
        
        Based on your qualifications, we'd like to invite you for an interview. 
        Please let us know if you're available and interested in this opportunity.
        
        {f"Job Description: {job.description}" if job else ""}
        
        Best regards,
        Recruitment Team
        """
        
        # Send the email
        return await self._send_email(candidate.email, subject, body)
    
    async def schedule_interview(self, candidate, date_time: str, job_id: Optional[int] = None) -> bool:
        """
        Send interview scheduling email to candidate
        """
        job_title = "our company"
        if job_id:
            # In a real app, you'd look up the job details
            job_title = f"the position (ID: {job_id})"
        
        subject = f"Interview Scheduled - {job_title}"
        
        # Parse the date_time string to a readable format
        try:
            interview_dt = datetime.fromisoformat(date_time)
            formatted_dt = interview_dt.strftime("%A, %B %d, %Y at %I:%M %p")
        except:
            formatted_dt = date_time  # Use as-is if parsing fails
        
        # Construct the email body
        body = f"""
        Dear {candidate.first_name} {candidate.last_name},
        
        Your interview for {job_title} has been scheduled for {formatted_dt}.
        
        Please let us know if you need to reschedule.
        
        Best regards,
        Recruitment Team
        """
        
        # Send the email
        return await self._send_email(candidate.email, subject, body)
    
    async def send_follow_up(self, candidate, message: str) -> bool:
        """
        Send a follow-up email to a candidate
        """
        subject = "Follow-up on your application"
        
        # Construct the email body
        body = f"""
        Dear {candidate.first_name} {candidate.last_name},
        
        {message}
        
        Best regards,
        Recruitment Team
        """
        
        # Send the email
        return await self._send_email(candidate.email, subject, body)
    
    async def _send_email(self, to_email: str, subject: str, body: str) -> bool:
        """
        Send an email using SMTP
        """
        if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
            # If SMTP is not configured, print the email and return True (for development)
            print(f"\n--- EMAIL ---\nTo: {to_email}\nSubject: {subject}\n\n{body}\n------------\n")
            return True
        
        # Create message
        message = MIMEMultipart()
        message["From"] = settings.SMTP_USER
        message["To"] = to_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        
        try:
            # Send the email
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                use_tls=True
            )
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False


email_service = EmailService() 