import json
from typing import Dict, Any, List
import PyPDF2
import ollama
from sentence_transformers import SentenceTransformer

class CVAnalyzerAgent:
    def __init__(self):
        """Initialize the CV Analyzer agent."""
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.ollama_model = "mistral"

    async def analyze_cv(self, cv_path: str) -> Dict[str, Any]:
        """
        Analyze a CV and extract key information.
        
        Args:
            cv_path (str): Path to the CV file (PDF)
            
        Returns:
            Dict[str, Any]: Structured CV data including:
                - name: Candidate's name
                - email: Contact email
                - phone: Contact phone
                - skills: List of skills
                - experience: List of work experience
                - education: List of education history
                - embedding: Vector embedding of the CV
        """
        try:
            # Extract text from PDF
            cv_text = self._extract_text_from_pdf(cv_path)
            
            # Generate embedding for the CV
            embedding = self.model.encode(cv_text)
            
            # Use Ollama to extract structured information
            prompt = f"""
            Analyze the following CV and extract key information in JSON format:
            
            {cv_text}
            
            Return a JSON object with the following structure:
            {{
                "name": "Full name",
                "email": "Email address",
                "phone": "Phone number",
                "skills": ["skill1", "skill2", ...],
                "experience": [
                    {{
                        "title": "Job title",
                        "company": "Company name",
                        "duration": "Duration",
                        "description": "Job description"
                    }},
                    ...
                ],
                "education": [
                    {{
                        "degree": "Degree name",
                        "institution": "Institution name",
                        "year": "Year completed"
                    }},
                    ...
                ]
            }}
            """
            
            response = ollama.generate(
                model=self.ollama_model,
                prompt=prompt,
                stream=False
            )
            
            # Parse the response
            try:
                cv_data = json.loads(response['response'])
            except json.JSONDecodeError:
                # Fallback to basic extraction if JSON parsing fails
                cv_data = self._extract_basic_info(cv_text)
            
            # Add the embedding to the CV data
            cv_data['embedding'] = embedding.tolist()
            
            return cv_data
            
        except Exception as e:
            print(f"Error analyzing CV: {str(e)}")
            # Return basic structure with empty values
            return {
                "name": "",
                "email": "",
                "phone": "",
                "skills": [],
                "experience": [],
                "education": [],
                "embedding": embedding.tolist() if 'embedding' in locals() else []
            }

    def _extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Args:
            pdf_path (str): Path to the PDF file
            
        Returns:
            str: Extracted text from the PDF
        """
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
        return text

    def _extract_basic_info(self, cv_text: str) -> Dict[str, Any]:
        """
        Fallback method to extract basic information from CV text.
        
        Args:
            cv_text (str): The CV text
            
        Returns:
            Dict[str, Any]: Basic CV data structure
        """
        # Split the text into lines
        lines = cv_text.split('\n')
        
        # Initialize the basic structure
        cv_data = {
            "name": "",
            "email": "",
            "phone": "",
            "skills": [],
            "experience": [],
            "education": []
        }
        
        # Try to find name (usually in the first few lines)
        for line in lines[:3]:
            if line.strip() and len(line.strip()) < 50:  # Names are usually short
                cv_data["name"] = line.strip()
                break
        
        # Look for email and phone
        for line in lines:
            line = line.strip().lower()
            if '@' in line and '.' in line:
                cv_data["email"] = line
            elif any(c.isdigit() for c in line) and len(line) > 8:
                cv_data["phone"] = line
        
        # Look for common section headers
        current_section = None
        current_experience = {}
        current_education = {}
        
        for line in lines:
            line = line.strip()
            
            # Identify sections
            if "experience" in line.lower() or "work" in line.lower():
                current_section = "experience"
            elif "education" in line.lower():
                current_section = "education"
            elif "skills" in line.lower():
                current_section = "skills"
            
            # Process the line based on the current section
            if current_section == "skills" and line and not line.endswith(":"):
                cv_data["skills"].append(line)
            elif current_section == "experience" and line:
                if "title" in line.lower() or "position" in line.lower():
                    if current_experience:
                        cv_data["experience"].append(current_experience)
                    current_experience = {"title": line}
                elif "company" in line.lower():
                    current_experience["company"] = line
                elif "duration" in line.lower():
                    current_experience["duration"] = line
                else:
                    current_experience["description"] = current_experience.get("description", "") + " " + line
            elif current_section == "education" and line:
                if "degree" in line.lower():
                    if current_education:
                        cv_data["education"].append(current_education)
                    current_education = {"degree": line}
                elif "institution" in line.lower():
                    current_education["institution"] = line
                elif "year" in line.lower():
                    current_education["year"] = line
        
        # Add the last experience and education entries
        if current_experience:
            cv_data["experience"].append(current_experience)
        if current_education:
            cv_data["education"].append(current_education)
        
        return cv_data 