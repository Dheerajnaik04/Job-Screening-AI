import ollama
from sentence_transformers import SentenceTransformer
import json
from typing import Dict, List, Any
import re

class JDAnalyzerAgent:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.ollama_model = "mistral"
        
    async def analyze_job_description(self, job_description: str) -> Dict[str, Any]:
        """
        Analyze a job description and extract key information.
        """
        # Extract sections using Ollama
        sections = await self._extract_sections(job_description)
        
        # Generate embeddings
        embedding = self._generate_embedding(job_description)
        
        # Structure the data
        structured_data = {
            "title": sections.get("title", ""),
            "description": job_description,
            "requirements": sections.get("requirements", []),
            "responsibilities": sections.get("responsibilities", []),
            "skills": sections.get("skills", []),
            "embedding": embedding.tolist()
        }
        
        return structured_data
    
    async def _extract_sections(self, text: str) -> Dict[str, List[str]]:
        """
        Extract different sections from the job description using Ollama.
        """
        prompt = f"""
        Analyze this job description and extract the following information in JSON format:
        1. Job title
        2. Requirements (as a list)
        3. Responsibilities (as a list)
        4. Required skills (as a list)
        
        Job Description:
        {text}
        
        Return only the JSON object with these keys: title, requirements, responsibilities, skills
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
    
    def _basic_extraction(self, text: str) -> Dict[str, List[str]]:
        """
        Basic extraction method as fallback.
        """
        sections = {
            "title": "",
            "requirements": [],
            "responsibilities": [],
            "skills": []
        }
        
        # Extract title (assuming it's the first line)
        lines = text.split('\n')
        if lines:
            sections["title"] = lines[0].strip()
        
        # Look for common section headers
        current_section = None
        for line in lines:
            line = line.lower().strip()
            if "requirements" in line or "qualifications" in line:
                current_section = "requirements"
            elif "responsibilities" in line:
                current_section = "responsibilities"
            elif "skills" in line:
                current_section = "skills"
            elif current_section and line and not line.endswith(':'):
                sections[current_section].append(line)
        
        return sections
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for the job description.
        """
        return self.model.encode(text)
    
    def calculate_skill_match(self, job_skills: List[str], candidate_skills: List[str]) -> float:
        """
        Calculate the skill match percentage between job and candidate.
        """
        if not job_skills or not candidate_skills:
            return 0.0
            
        # Convert to sets for comparison
        job_skills_set = set(skill.lower() for skill in job_skills)
        candidate_skills_set = set(skill.lower() for skill in candidate_skills)
        
        # Calculate match percentage
        matching_skills = job_skills_set.intersection(candidate_skills_set)
        match_percentage = len(matching_skills) / len(job_skills_set) * 100
        
        return match_percentage 