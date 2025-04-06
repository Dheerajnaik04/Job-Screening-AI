from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any
import json
from contextlib import asynccontextmanager
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.db_manager import DatabaseManager, init_db
from src.agents.jd_analyzer import JDAnalyzerAgent
from src.agents.cv_analyzer import CVAnalyzerAgent
from src.agents.matcher import MatcherAgent
from src.agents.scheduler import SchedulerAgent

# Initialize agents
jd_analyzer = JDAnalyzerAgent()
cv_analyzer = CVAnalyzerAgent()
matcher = MatcherAgent()
scheduler = SchedulerAgent()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    pass

# Initialize FastAPI app
app = FastAPI(
    title="Job Screening AI",
    description="""
    An AI-powered job screening system that automates the recruitment process.
    
    ## Features
    * Job Description Analysis
    * CV Analysis
    * Smart Candidate Matching
    * Interview Scheduling
    
    ## API Documentation
    Visit `/docs` for the complete API documentation.
    """,
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Job Screening AI API",
        "documentation": "/docs",
        "endpoints": {
            "analyze_job": "/analyze-job",
            "analyze_cv": "/analyze-cv",
            "match_candidate": "/match-candidate",
            "schedule_interview": "/schedule-interview/{match_id}",
            "job_matches": "/job-matches/{job_id}",
            "candidate_matches": "/candidate-matches/{candidate_id}"
        }
    }

@app.post("/analyze-job")
async def analyze_job(job_description: str, session: AsyncSession = Depends(DatabaseManager.get_session)):
    try:
        # Analyze job description
        job_data = await jd_analyzer.analyze_job_description(job_description)
        
        # Ensure description is included in job_data
        if "description" not in job_data:
            job_data["description"] = job_description
        
        # Create job in database
        job = await DatabaseManager.create_job(session, job_data)
        
        return {"job_id": job.id, "job_data": job_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-cv")
async def analyze_cv(cv_path: str, session: AsyncSession = Depends(DatabaseManager.get_session)):
    try:
        # Analyze CV
        cv_data = await cv_analyzer.analyze_cv(cv_path)
        
        # Create candidate in database
        candidate = await DatabaseManager.create_candidate(session, cv_data)
        
        return {"candidate_id": candidate.id, "cv_data": cv_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/match-candidate")
async def match_candidate(
    job_id: int,
    candidate_id: int,
    session: AsyncSession = Depends(DatabaseManager.get_session)
):
    try:
        # Get job and candidate
        job = await DatabaseManager.get_job(session, job_id)
        candidate = await DatabaseManager.get_candidate(session, candidate_id)
        
        if not job or not candidate:
            raise HTTPException(status_code=404, detail="Job or candidate not found")
        
        # Calculate match score
        match_score, match_details = matcher.calculate_match_score(
            job.__dict__,
            candidate.__dict__
        )
        
        # Create match in database
        match_data = {
            "job_id": job_id,
            "candidate_id": candidate_id,
            "match_score": match_score,
            "match_details": match_details,
            "status": "pending"
        }
        match = await DatabaseManager.create_match(session, match_data)
        
        return {
            "match_id": match.id,
            "match_score": match_score,
            "match_details": match_details
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/schedule-interview/{match_id}")
async def schedule_interview(
    match_id: int,
    session: AsyncSession = Depends(DatabaseManager.get_session)
):
    try:
        # Get match
        match = await DatabaseManager.get_match(session, match_id)
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")
        
        # Get job and candidate
        job = await DatabaseManager.get_job(session, match.job_id)
        candidate = await DatabaseManager.get_candidate(session, match.candidate_id)
        
        # Schedule interview
        interview_data = await scheduler.schedule_interview(
            job.__dict__,
            candidate.__dict__,
            match.match_details
        )
        
        # Create interview in database
        interview_data["match_id"] = match_id
        interview_data["status"] = "scheduled"
        interview = await DatabaseManager.create_interview(session, interview_data)
        
        return {
            "interview_id": interview.id,
            "interview_details": interview_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/job-matches/{job_id}")
async def get_job_matches(
    job_id: int,
    session: AsyncSession = Depends(DatabaseManager.get_session)
):
    try:
        matches = await DatabaseManager.get_job_matches(session, job_id)
        return {"matches": matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/candidate-matches/{candidate_id}")
async def get_candidate_matches(
    candidate_id: int,
    session: AsyncSession = Depends(DatabaseManager.get_session)
):
    try:
        matches = await DatabaseManager.get_candidate_matches(session, candidate_id)
        return {"matches": matches}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True) 