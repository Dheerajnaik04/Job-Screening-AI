import json
from typing import Dict, Any
import ollama
from sentence_transformers import SentenceTransformer

class JDAnalyzerAgent:
    def __init__(self):
        """Initialize the JD Analyzer agent."""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.ollama_model = "mistral"

    async def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """
        Analyze a job description and extract key information.
        
        Args:
            job_description (str): The job description text
            
        Returns:
            Dict[str, Any]: Structured job data including:
                - title: Job title
                - description: Original job description
                - required_skills: List of required skills
                - preferred_skills: List of preferred skills
                - experience: Required experience
                - education: Required education
                - responsibilities: List of key responsibilities
                - embedding: Vector embedding of the job description
        """
        try:
            # Generate embedding for the job description
            embedding = self.model.encode(job_description)
            
            # Use Ollama to extract structured information
            prompt = f"""
            Analyze the following job description and extract key information in JSON format:
            
            {job_description}
            
            Return a JSON object with the following structure:
            {{
                "title": "Job title",
                "required_skills": ["skill1", "skill2", ...],
                "preferred_skills": ["skill1", "skill2", ...],
                "experience": "Required experience description",
                "education": "Required education description",
                "responsibilities": ["responsibility1", "responsibility2", ...]
            }}
            """
            
            response = ollama.generate(
                model=self.ollama_model,
                prompt=prompt,
                stream=False
            )
            
            # Parse the response
            try:
                job_data = json.loads(response['response'])
            except json.JSONDecodeError:
                # Fallback to basic extraction if JSON parsing fails
                job_data = self._extract_basic_info(job_description)
            
            # Add the embedding and description to the job data
            job_data['embedding'] = embedding.tolist()
            job_data['description'] = job_description
            
            return job_data
            
        except Exception as e:
            print(f"Error analyzing job description: {str(e)}")
            # Return basic structure with empty values
            return {
                "title": "",
                "description": job_description,
                "required_skills": [],
                "preferred_skills": [],
                "experience": "",
                "education": "",
                "responsibilities": [],
                "embedding": embedding.tolist() if 'embedding' in locals() else []
            }

    def _extract_basic_info(self, job_description: str) -> Dict[str, Any]:
        """
        Fallback method to extract basic information from job description.
        
        Args:
            job_description (str): The job description text
            
        Returns:
            Dict[str, Any]: Basic job data structure
        """
        # Split the description into lines
        lines = job_description.split('\n')
        
        # Initialize the basic structure
        job_data = {
            "title": "",
            "required_skills": [],
            "preferred_skills": [],
            "experience": "",
            "education": "",
            "responsibilities": []
        }
        
        # Try to find the job title (usually in the first few lines)
        for line in lines[:3]:
            if line.strip() and len(line.strip()) < 100:  # Job titles are usually short
                job_data["title"] = line.strip()
                break
        
        # Look for common section headers
        current_section = None
        for line in lines:
            line = line.strip().lower()
            
            # Identify sections
            if "requirements" in line or "qualifications" in line:
                current_section = "requirements"
            elif "responsibilities" in line or "duties" in line:
                current_section = "responsibilities"
            elif "education" in line:
                current_section = "education"
            elif "experience" in line:
                current_section = "experience"
            
            # Process the line based on the current section
            if current_section == "requirements" and line and not line.endswith(":"):
                if "preferred" in line:
                    job_data["preferred_skills"].append(line)
                else:
                    job_data["required_skills"].append(line)
            elif current_section == "responsibilities" and line and not line.endswith(":"):
                job_data["responsibilities"].append(line)
            elif current_section == "education" and line and not line.endswith(":"):
                job_data["education"] = line
            elif current_section == "experience" and line and not line.endswith(":"):
                job_data["experience"] = line
        
        return job_data 