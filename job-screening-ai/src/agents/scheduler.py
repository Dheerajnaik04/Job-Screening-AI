from typing import Dict, List, Any
import ollama
from datetime import datetime, timedelta
import json
import re

class SchedulerAgent:
    def __init__(self):
        self.ollama_model = "mistral"
        
    async def schedule_interview(
        self,
        job_data: Dict[str, Any],
        candidate_data: Dict[str, Any],
        match_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Schedule an interview for a matched candidate.
        """
        # Generate interview details
        interview_details = await self._generate_interview_details(
            job_data,
            candidate_data,
            match_details
        )
        
        # Generate email content
        email_content = await self._generate_email_content(
            job_data,
            candidate_data,
            interview_details
        )
        
        return {
            "interview_details": interview_details,
            "email_content": email_content
        }
    
    async def _generate_interview_details(
        self,
        job_data: Dict[str, Any],
        candidate_data: Dict[str, Any],
        match_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate interview details using Ollama.
        """
        prompt = f"""
        Generate interview details for a candidate based on the following information:
        
        Job Title: {job_data['title']}
        Candidate Name: {candidate_data['name']}
        Match Score: {match_details['overall_score']}%
        
        Generate a JSON object with the following structure:
        {{
            "suggested_dates": ["YYYY-MM-DD HH:MM"],  # List of 3 suggested dates/times
            "duration": 60,  # Interview duration in minutes
            "interview_type": "online",  # online, in-person, or phone
            "interview_format": "technical",  # technical, behavioral, or both
            "topics_to_cover": ["topic1", "topic2"],  # List of topics to cover
            "interviewers": ["interviewer1", "interviewer2"]  # List of suggested interviewers
        }}
        
        Consider the job requirements and candidate's experience when suggesting topics.
        """
        
        response = await ollama.chat(
            model=self.ollama_model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            # Extract JSON from response
            json_str = response["message"]["content"]
            # Clean the response to ensure it's valid JSON
            json_str = re.sub(r'```json\s*|\s*```', '', json_str)
            interview_details = json.loads(json_str)
            
            # Validate and adjust dates
            interview_details["suggested_dates"] = self._validate_dates(
                interview_details["suggested_dates"]
            )
            
            return interview_details
        except json.JSONDecodeError:
            # Fallback to default interview details
            return self._get_default_interview_details()
    
    async def _generate_email_content(
        self,
        job_data: Dict[str, Any],
        candidate_data: Dict[str, Any],
        interview_details: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Generate email content for interview invitation.
        """
        prompt = f"""
        Generate an email for interview invitation with the following information:
        
        Job Title: {job_data['title']}
        Candidate Name: {candidate_data['name']}
        Candidate Email: {candidate_data['email']}
        
        Interview Details:
        - Duration: {interview_details['duration']} minutes
        - Type: {interview_details['interview_type']}
        - Format: {interview_details['interview_format']}
        - Suggested Dates: {', '.join(interview_details['suggested_dates'])}
        - Topics: {', '.join(interview_details['topics_to_cover'])}
        
        Generate two versions of the email:
        1. A formal version
        2. A friendly version
        
        Return as JSON with keys: "formal" and "friendly"
        """
        
        response = await ollama.chat(
            model=self.ollama_model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            # Extract JSON from response
            json_str = response["message"]["content"]
            # Clean the response to ensure it's valid JSON
            json_str = re.sub(r'```json\s*|\s*```', '', json_str)
            return json.loads(json_str)
        except json.JSONDecodeError:
            # Fallback to default email templates
            return self._get_default_email_templates(
                job_data,
                candidate_data,
                interview_details
            )
    
    def _validate_dates(self, dates: List[str]) -> List[str]:
        """
        Validate and adjust suggested dates to ensure they're in the future.
        """
        valid_dates = []
        current_time = datetime.now()
        
        for date_str in dates:
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
                if date > current_time:
                    valid_dates.append(date_str)
            except ValueError:
                continue
        
        # If no valid dates, generate some default ones
        if not valid_dates:
            for i in range(1, 4):
                future_date = current_time + timedelta(days=i)
                valid_dates.append(future_date.strftime("%Y-%m-%d %H:%M"))
        
        return valid_dates
    
    def _get_default_interview_details(self) -> Dict[str, Any]:
        """
        Get default interview details as fallback.
        """
        current_time = datetime.now()
        suggested_dates = []
        
        for i in range(1, 4):
            future_date = current_time + timedelta(days=i)
            suggested_dates.append(future_date.strftime("%Y-%m-%d %H:%M"))
        
        return {
            "suggested_dates": suggested_dates,
            "duration": 60,
            "interview_type": "online",
            "interview_format": "technical",
            "topics_to_cover": ["Technical Skills", "Problem Solving", "Experience"],
            "interviewers": ["Technical Lead", "HR Manager"]
        }
    
    def _get_default_email_templates(
        self,
        job_data: Dict[str, Any],
        candidate_data: Dict[str, Any],
        interview_details: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Get default email templates as fallback.
        """
        formal_template = f"""
        Dear {candidate_data['name']},

        We are pleased to invite you for an interview for the position of {job_data['title']}.

        Interview Details:
        - Duration: {interview_details['duration']} minutes
        - Type: {interview_details['interview_type']}
        - Format: {interview_details['interview_format']}
        
        Suggested Dates:
        {chr(10).join(f'- {date}' for date in interview_details['suggested_dates'])}

        Topics to be covered:
        {chr(10).join(f'- {topic}' for topic in interview_details['topics_to_cover'])}

        Please let us know your preferred date and time.

        Best regards,
        Hiring Team
        """
        
        friendly_template = f"""
        Hi {candidate_data['name']},

        Great news! We'd love to chat with you about the {job_data['title']} position.

        We've got some time slots available:
        {chr(10).join(f'- {date}' for date in interview_details['suggested_dates'])}

        It'll be a {interview_details['duration']}-minute {interview_details['interview_type']} interview.
        We'll talk about your experience and some technical stuff.

        Let us know which time works best for you!

        Looking forward to meeting you,
        The Team
        """
        
        return {
            "formal": formal_template,
            "friendly": friendly_template
        } 