from typing import Dict, List, Any, Tuple
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class MatcherAgent:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def calculate_match_score(
        self,
        job_data: Dict[str, Any],
        candidate_data: Dict[str, Any]
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate the overall match score between a job and a candidate.
        Returns the match score and detailed matching information.
        """
        # Calculate different aspects of the match
        embedding_score = self._calculate_embedding_similarity(
            job_data["embedding"],
            candidate_data["embedding"]
        )
        
        skill_score = self._calculate_skill_match(
            job_data["skills"],
            candidate_data["skills"]
        )
        
        experience_score = self._calculate_experience_match(
            job_data["requirements"],
            candidate_data["experience"]
        )
        
        # Calculate weighted average
        weights = {
            "embedding": 0.4,
            "skills": 0.3,
            "experience": 0.3
        }
        
        overall_score = (
            embedding_score * weights["embedding"] +
            skill_score * weights["skills"] +
            experience_score * weights["experience"]
        )
        
        # Prepare detailed matching information
        match_details = {
            "overall_score": overall_score,
            "embedding_score": embedding_score,
            "skill_score": skill_score,
            "experience_score": experience_score,
            "matching_skills": self._get_matching_skills(
                job_data["skills"],
                candidate_data["skills"]
            ),
            "matching_experience": self._get_matching_experience(
                job_data["requirements"],
                candidate_data["experience"]
            )
        }
        
        return overall_score, match_details
    
    def _calculate_embedding_similarity(
        self,
        job_embedding: List[float],
        candidate_embedding: List[float]
    ) -> float:
        """
        Calculate cosine similarity between job and candidate embeddings.
        """
        job_embedding = np.array(job_embedding).reshape(1, -1)
        candidate_embedding = np.array(candidate_embedding).reshape(1, -1)
        
        similarity = cosine_similarity(job_embedding, candidate_embedding)[0][0]
        return float(similarity * 100)  # Convert to percentage
    
    def _calculate_skill_match(
        self,
        job_skills: List[str],
        candidate_skills: List[str]
    ) -> float:
        """
        Calculate the percentage of matching skills.
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
    
    def _calculate_experience_match(
        self,
        job_requirements: List[str],
        candidate_experience: List[str]
    ) -> float:
        """
        Calculate the percentage of matching experience.
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
    
    def _get_matching_skills(
        self,
        job_skills: List[str],
        candidate_skills: List[str]
    ) -> List[str]:
        """
        Get the list of matching skills between job and candidate.
        """
        job_skills_set = set(skill.lower() for skill in job_skills)
        candidate_skills_set = set(skill.lower() for skill in candidate_skills)
        
        return list(job_skills_set.intersection(candidate_skills_set))
    
    def _get_matching_experience(
        self,
        job_requirements: List[str],
        candidate_experience: List[str]
    ) -> List[str]:
        """
        Get the list of matching experience between job requirements and candidate experience.
        """
        requirements_set = set(req.lower() for req in job_requirements)
        experience_set = set(exp.lower() for exp in candidate_experience)
        
        return list(requirements_set.intersection(experience_set))
    
    def get_match_summary(self, match_details: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the match.
        """
        summary = f"""
        Overall Match Score: {match_details['overall_score']:.2f}%
        
        Detailed Scores:
        - Semantic Similarity: {match_details['embedding_score']:.2f}%
        - Skills Match: {match_details['skill_score']:.2f}%
        - Experience Match: {match_details['experience_score']:.2f}%
        
        Matching Skills:
        {', '.join(match_details['matching_skills'])}
        
        Matching Experience:
        {', '.join(match_details['matching_experience'])}
        """
        
        return summary 