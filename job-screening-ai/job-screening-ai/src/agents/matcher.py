from typing import Dict, Any, Tuple, List
import numpy as np
from sentence_transformers import SentenceTransformer

class MatcherAgent:
    def __init__(self):
        """Initialize the Matcher agent."""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def calculate_match_score(self, job_data: Dict[str, Any], cv_data: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate the match score between a job and a candidate.
        
        Args:
            job_data (Dict[str, Any]): Structured job data
            cv_data (Dict[str, Any]): Structured CV data
            
        Returns:
            Tuple[float, Dict[str, Any]]: Match score (0-100) and detailed matching information
        """
        try:
            # Calculate different aspects of the match
            embedding_similarity = self._calculate_embedding_similarity(
                job_data['embedding'],
                cv_data['embedding']
            )
            
            skill_match = self._calculate_skill_match(
                job_data['required_skills'] + job_data['preferred_skills'],
                cv_data['skills']
            )
            
            experience_match = self._calculate_experience_match(
                job_data['experience'],
                cv_data['experience']
            )
            
            # Calculate weighted average score
            weights = {
                'embedding': 0.4,
                'skills': 0.4,
                'experience': 0.2
            }
            
            match_score = (
                embedding_similarity * weights['embedding'] +
                skill_match * weights['skills'] +
                experience_match * weights['experience']
            ) * 100
            
            # Prepare detailed matching information
            match_details = {
                'overall_score': match_score,
                'embedding_similarity': embedding_similarity * 100,
                'skill_match': skill_match * 100,
                'experience_match': experience_match * 100,
                'matching_skills': self._get_matching_skills(
                    job_data['required_skills'] + job_data['preferred_skills'],
                    cv_data['skills']
                ),
                'matching_experience': self._get_matching_experience(
                    job_data['experience'],
                    cv_data['experience']
                )
            }
            
            return match_score, match_details
            
        except Exception as e:
            print(f"Error calculating match score: {str(e)}")
            return 0.0, {
                'overall_score': 0.0,
                'embedding_similarity': 0.0,
                'skill_match': 0.0,
                'experience_match': 0.0,
                'matching_skills': [],
                'matching_experience': []
            }

    def _calculate_embedding_similarity(self, job_embedding: List[float], cv_embedding: List[float]) -> float:
        """
        Calculate cosine similarity between job and CV embeddings.
        
        Args:
            job_embedding (List[float]): Job description embedding
            cv_embedding (List[float]): CV embedding
            
        Returns:
            float: Similarity score between 0 and 1
        """
        try:
            job_vec = np.array(job_embedding)
            cv_vec = np.array(cv_embedding)
            
            # Calculate cosine similarity
            similarity = np.dot(job_vec, cv_vec) / (np.linalg.norm(job_vec) * np.linalg.norm(cv_vec))
            
            # Ensure the score is between 0 and 1
            return max(0.0, min(1.0, similarity))
            
        except Exception as e:
            print(f"Error calculating embedding similarity: {str(e)}")
            return 0.0

    def _calculate_skill_match(self, job_skills: List[str], cv_skills: List[str]) -> float:
        """
        Calculate the percentage of matching skills.
        
        Args:
            job_skills (List[str]): Required and preferred skills from job
            cv_skills (List[str]): Skills from CV
            
        Returns:
            float: Match percentage between 0 and 1
        """
        try:
            if not job_skills:
                return 0.0
                
            # Convert skills to lowercase for comparison
            job_skills = [skill.lower() for skill in job_skills]
            cv_skills = [skill.lower() for skill in cv_skills]
            
            # Count matching skills
            matching_skills = sum(1 for skill in job_skills if skill in cv_skills)
            
            return matching_skills / len(job_skills)
            
        except Exception as e:
            print(f"Error calculating skill match: {str(e)}")
            return 0.0

    def _calculate_experience_match(self, job_experience: str, cv_experience: List[Dict[str, Any]]) -> float:
        """
        Calculate the percentage of matching experience.
        
        Args:
            job_experience (str): Required experience from job
            cv_experience (List[Dict[str, Any]]): Experience from CV
            
        Returns:
            float: Match percentage between 0 and 1
        """
        try:
            if not job_experience or not cv_experience:
                return 0.0
                
            # Generate embeddings for job experience and CV experience
            job_exp_embedding = self.model.encode(job_experience)
            cv_exp_embeddings = [
                self.model.encode(exp['description'])
                for exp in cv_experience
                if 'description' in exp
            ]
            
            if not cv_exp_embeddings:
                return 0.0
                
            # Calculate similarity with each experience entry
            similarities = [
                np.dot(job_exp_embedding, cv_exp_embedding) / 
                (np.linalg.norm(job_exp_embedding) * np.linalg.norm(cv_exp_embedding))
                for cv_exp_embedding in cv_exp_embeddings
            ]
            
            # Take the highest similarity score
            return max(0.0, min(1.0, max(similarities)))
            
        except Exception as e:
            print(f"Error calculating experience match: {str(e)}")
            return 0.0

    def _get_matching_skills(self, job_skills: List[str], cv_skills: List[str]) -> List[str]:
        """
        Get a list of skills that match between job and CV.
        
        Args:
            job_skills (List[str]): Required and preferred skills from job
            cv_skills (List[str]): Skills from CV
            
        Returns:
            List[str]: List of matching skills
        """
        try:
            # Convert skills to lowercase for comparison
            job_skills = [skill.lower() for skill in job_skills]
            cv_skills = [skill.lower() for skill in cv_skills]
            
            # Find matching skills
            matching_skills = [skill for skill in job_skills if skill in cv_skills]
            
            return matching_skills
            
        except Exception as e:
            print(f"Error getting matching skills: {str(e)}")
            return []

    def _get_matching_experience(self, job_experience: str, cv_experience: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Get a list of experience entries that match the job requirements.
        
        Args:
            job_experience (str): Required experience from job
            cv_experience (List[Dict[str, Any]]): Experience from CV
            
        Returns:
            List[Dict[str, Any]]: List of matching experience entries
        """
        try:
            if not job_experience or not cv_experience:
                return []
                
            # Generate embedding for job experience
            job_exp_embedding = self.model.encode(job_experience)
            
            # Calculate similarity for each experience entry
            matching_experience = []
            for exp in cv_experience:
                if 'description' in exp:
                    exp_embedding = self.model.encode(exp['description'])
                    similarity = np.dot(job_exp_embedding, exp_embedding) / (
                        np.linalg.norm(job_exp_embedding) * np.linalg.norm(exp_embedding)
                    )
                    
                    if similarity > 0.5:  # Threshold for considering it a match
                        matching_experience.append(exp)
            
            return matching_experience
            
        except Exception as e:
            print(f"Error getting matching experience: {str(e)}")
            return [] 