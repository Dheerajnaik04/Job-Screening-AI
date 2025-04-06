import ollama
from sentence_transformers import SentenceTransformer
import json
from typing import Dict, List, Any
import re
from PyPDF2 import PdfReader
import os

class CVAnalyzerAgent:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.ollama_model = "mistral"
        
    async def analyze_cv(self, cv_path: str) -> Dict[str, Any]:
        """
        Analyze a CV and extract key information.
        """
        # Extract text from PDF
        text = self._extract_text_from_pdf(cv_path)
        
        # Extract information using Ollama
        cv_data = await self._extract_cv_data(text)
        
        # Generate embedding
        embedding = self._generate_embedding(text)
        
        # Structure the data
        structured_data = {
            "cv_id": os.path.basename(cv_path),
            "name": cv_data.get("name", ""),
            "email": cv_data.get("email", ""),
            "education": cv_data.get("education", []),
            "experience": cv_data.get("experience", []),
            "skills": cv_data.get("skills", []),
            "embedding": embedding.tolist()
        }
        
        return structured_data
    
    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file.
        """
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""
    
    async def _extract_cv_data(self, text: str) -> Dict[str, Any]:
        """
        Extract structured information from CV text using Ollama.
        """
        prompt = f"""
        Analyze this CV and extract the following information in JSON format:
        1. Full name
        2. Email address
        3. Education history (list of degrees with institution, year, and field)
        4. Work experience (list of jobs with company, duration, and key responsibilities)
        5. Skills (list of technical and soft skills)
        
        CV Text:
        {text}
        
        Return only the JSON object with these keys: name, email, education, experience, skills
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
            # Fallback to basic extraction if JSON parsing fails
            return self._basic_extraction(text)
    
    def _basic_extraction(self, text: str) -> Dict[str, Any]:
        """
        Basic extraction method as fallback.
        """
        data = {
            "name": "",
            "email": "",
            "education": [],
            "experience": [],
            "skills": []
        }
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            data["email"] = email_match.group()
        
        # Extract name (assuming it's at the beginning of the CV)
        lines = text.split('\n')
        if lines:
            data["name"] = lines[0].strip()
        
        # Look for common section headers
        current_section = None
        for line in lines:
            line = line.lower().strip()
            if "education" in line:
                current_section = "education"
            elif "experience" in line or "work" in line:
                current_section = "experience"
            elif "skills" in line:
                current_section = "skills"
            elif current_section and line and not line.endswith(':'):
                data[current_section].append(line)
        
        return data
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for the CV text.
        """
        return self.model.encode(text)
    
    def calculate_experience_match(self, job_requirements: List[str], candidate_experience: List[str]) -> float:
        """
        Calculate the experience match percentage between job requirements and candidate experience.
        """
        if not job_requirements or not candidate_experience:
            return 0.0
            
        # Convert to sets for comparison
        requirements_set = set(req.lower() for req in job_requirements)
        experience_set = set(exp.lower() for exp in candidate_experience)
        
        # Calculate match percentage
        matching_experience = requirements_set.intersection(experience_set)
        match_percentage = len(matching_experience) / len(requirements_set) * 100
        
        return match_percentage 