import json
from typing import Dict, Any
from datetime import datetime, timedelta
import ollama

class SchedulerAgent:
    def __init__(self):
        """Initialize the Scheduler agent."""
        self.ollama_model = "mistral"

    async def schedule_interview(self, job_data: Dict[str, Any], cv_data: Dict[str, Any], match_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Schedule an interview for a matched candidate.
        
        Args:
            job_data (Dict[str, Any]): Structured job data
            cv_data (Dict[str, Any]): Structured CV data
            match_details (Dict[str, Any]): Matching details
            
        Returns:
            Dict[str, Any]: Interview details including:
                - interview_details: Date, time, duration, type, format
                - topics: Topics to cover
                - interviewers: List of interviewers
                - email_content: Email content for the invitation
        """
        try:
            # Generate interview details
            interview_details = await self._generate_interview_details(
                job_data,
                cv_data,
                match_details
            )
            
            # Generate email content
            email_content = await self._generate_email_content(
                job_data,
                cv_data,
                interview_details
            )
            
            return {
                "interview_details": interview_details,
                "email_content": email_content
            }
            
        except Exception as e:
            print(f"Error scheduling interview: {str(e)}")
            # Return default interview details
            return {
                "interview_details": self._get_default_interview_details(),
                "email_content": self._get_default_email_templates()
            }

    async def _generate_interview_details(self, job_data: Dict[str, Any], cv_data: Dict[str, Any], match_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate interview details using Ollama.
        
        Args:
            job_data (Dict[str, Any]): Structured job data
            cv_data (Dict[str, Any]): Structured CV data
            match_details (Dict[str, Any]): Matching details
            
        Returns:
            Dict[str, Any]: Interview details
        """
        try:
            prompt = f"""
            Generate interview details for a candidate based on the following information:
            
            Job Title: {job_data['title']}
            Candidate Name: {cv_data['name']}
            Match Score: {match_details['overall_score']}%
            
            Return a JSON object with the following structure:
            {{
                "date": "YYYY-MM-DD",
                "time": "HH:MM",
                "duration": "Duration in minutes",
                "type": "Interview type (e.g., Technical, HR, etc.)",
                "format": "Interview format (e.g., Online, In-person)",
                "topics": ["Topic 1", "Topic 2", ...],
                "interviewers": ["Interviewer 1", "Interviewer 2", ...]
            }}
            
            Make sure the date is in the future and the time is during business hours (9 AM - 5 PM).
            """
            
            response = ollama.generate(
                model=self.ollama_model,
                prompt=prompt,
                stream=False
            )
            
            # Parse the response
            try:
                interview_details = json.loads(response['response'])
                # Validate and adjust dates if necessary
                interview_details = self._validate_dates(interview_details)
                return interview_details
            except json.JSONDecodeError:
                return self._get_default_interview_details()
                
        except Exception as e:
            print(f"Error generating interview details: {str(e)}")
            return self._get_default_interview_details()

    async def _generate_email_content(self, job_data: Dict[str, Any], cv_data: Dict[str, Any], interview_details: Dict[str, Any]) -> Dict[str, str]:
        """
        Generate email content for the interview invitation.
        
        Args:
            job_data (Dict[str, Any]): Structured job data
            cv_data (Dict[str, Any]): Structured CV data
            interview_details (Dict[str, Any]): Interview details
            
        Returns:
            Dict[str, str]: Email content with subject and body
        """
        try:
            prompt = f"""
            Generate an email invitation for a job interview with the following details:
            
            Job Title: {job_data['title']}
            Candidate Name: {cv_data['name']}
            Interview Date: {interview_details['date']}
            Interview Time: {interview_details['time']}
            Duration: {interview_details['duration']}
            Format: {interview_details['format']}
            
            Return a JSON object with the following structure:
            {{
                "subject": "Email subject line",
                "body": "Email body content"
            }}
            
            Make the email professional yet friendly, and include all necessary details.
            """
            
            response = ollama.generate(
                model=self.ollama_model,
                prompt=prompt,
                stream=False
            )
            
            # Parse the response
            try:
                email_content = json.loads(response['response'])
                return email_content
            except json.JSONDecodeError:
                return self._get_default_email_templates()
                
        except Exception as e:
            print(f"Error generating email content: {str(e)}")
            return self._get_default_email_templates()

    def _validate_dates(self, interview_details: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and adjust interview dates if necessary.
        
        Args:
            interview_details (Dict[str, Any]): Interview details
            
        Returns:
            Dict[str, Any]: Validated interview details
        """
        try:
            # Parse the date and time
            date_str = interview_details['date']
            time_str = interview_details['time']
            
            # Combine date and time
            datetime_str = f"{date_str} {time_str}"
            interview_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
            
            # Check if the date is in the future
            if interview_datetime < datetime.now():
                # Add 1 day to the date
                interview_datetime = interview_datetime + timedelta(days=1)
                
                # Update the interview details
                interview_details['date'] = interview_datetime.strftime("%Y-%m-%d")
                interview_details['time'] = interview_datetime.strftime("%H:%M")
            
            return interview_details
            
        except Exception as e:
            print(f"Error validating dates: {str(e)}")
            return self._get_default_interview_details()

    def _get_default_interview_details(self) -> Dict[str, Any]:
        """
        Get default interview details.
        
        Returns:
            Dict[str, Any]: Default interview details
        """
        # Get tomorrow's date
        tomorrow = datetime.now() + timedelta(days=1)
        
        return {
            "date": tomorrow.strftime("%Y-%m-%d"),
            "time": "10:00",
            "duration": "60",
            "type": "Technical",
            "format": "Online",
            "topics": [
                "Technical skills",
                "Problem-solving abilities",
                "Previous experience",
                "Project discussions"
            ],
            "interviewers": [
                "Technical Lead",
                "HR Manager"
            ]
        }

    def _get_default_email_templates(self) -> Dict[str, str]:
        """
        Get default email templates.
        
        Returns:
            Dict[str, str]: Default email templates
        """
        return {
            "subject": "Interview Invitation - Technical Position",
            "body": """
            Dear Candidate,
            
            Thank you for your interest in the position. We would like to invite you for an interview.
            
            Date: {date}
            Time: {time}
            Duration: {duration} minutes
            Format: {format}
            
            Please confirm your availability for this interview.
            
            Best regards,
            Hiring Team
            """
        } 