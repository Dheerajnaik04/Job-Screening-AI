import asyncio
import os
from typing import List, Dict, Any
import pandas as pd
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from agents.jd_analyzer import JDAnalyzerAgent
from agents.cv_analyzer import CVAnalyzerAgent
from agents.matcher import MatcherAgent
from agents.scheduler import SchedulerAgent
from database.db_manager import DatabaseManager, init_db

app = FastAPI(title="AI-Powered Job Screening System")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
jd_analyzer = JDAnalyzerAgent()
cv_analyzer = CVAnalyzerAgent()
matcher = MatcherAgent()
scheduler = SchedulerAgent()

@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup."""
    await init_db()

@app.post("/analyze-job")
async def analyze_job(job_description: str):
    """Analyze a job description."""
    job_data = await jd_analyzer.analyze_job_description(job_description)
    return job_data

@app.post("/analyze-cv")
async def analyze_cv(cv_file: UploadFile = File(...)):
    """Analyze a CV file."""
    # Save the uploaded file temporarily
    temp_path = f"temp_{cv_file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            content = await cv_file.read()
            buffer.write(content)
        
        # Analyze the CV
        cv_data = await cv_analyzer.analyze_cv(temp_path)
        return cv_data
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/match-candidate")
async def match_candidate(job_id: int, cv_file: UploadFile = File(...)):
    """Match a candidate with a job."""
    # Save and analyze the CV
    temp_path = f"temp_{cv_file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            content = await cv_file.read()
            buffer.write(content)
        
        cv_data = await cv_analyzer.analyze_cv(temp_path)
        
        # Get job data from database
        async with DatabaseManager.get_session() as session:
            job = await session.get(Job, job_id)
            if not job:
                return {"error": "Job not found"}
            
            # Calculate match score
            match_score, match_details = matcher.calculate_match_score(
                job.__dict__,
                cv_data
            )
            
            # If match score is above threshold, schedule interview
            if match_score >= 80:
                interview_data = await scheduler.schedule_interview(
                    job.__dict__,
                    cv_data,
                    match_details
                )
                
                # Save match and interview data
                match = await DatabaseManager.create_match(session, {
                    "job_id": job_id,
                    "candidate_data": cv_data,
                    "match_score": match_score,
                    "match_details": match_details
                })
                
                interview = await DatabaseManager.create_interview(session, {
                    "match_id": match.id,
                    **interview_data["interview_details"]
                })
                
                return {
                    "match_score": match_score,
                    "match_details": match_details,
                    "interview_data": interview_data
                }
            
            return {
                "match_score": match_score,
                "match_details": match_details,
                "interview_data": None
            }
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/job-matches/{job_id}")
async def get_job_matches(job_id: int):
    """Get all matches for a job."""
    async with DatabaseManager.get_session() as session:
        matches = await DatabaseManager.get_job_matches(session, job_id)
        return matches

@app.get("/candidate-matches/{candidate_id}")
async def get_candidate_matches(candidate_id: int):
    """Get all matches for a candidate."""
    async with DatabaseManager.get_session() as session:
        matches = await DatabaseManager.get_candidate_matches(session, candidate_id)
        return matches

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 