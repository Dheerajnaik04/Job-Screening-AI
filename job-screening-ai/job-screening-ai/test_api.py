import requests
import json

BASE_URL = "http://localhost:8000"

def test_analyze_job():
    url = f"{BASE_URL}/analyze-job"
    params = {
        "job_description": "We are looking for a Python developer with experience in FastAPI and machine learning. The ideal candidate should have 3+ years of experience in web development and be familiar with SQL databases."
    }
    response = requests.post(url, params=params)
    print("Analyze Job Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json().get("job_id")

def test_analyze_cv():
    url = f"{BASE_URL}/analyze-cv"
    params = {
        "cv_path": "Dataset/CVs1/CV1.pdf"  # Update this path to a valid CV file
    }
    response = requests.post(url, params=params)
    print("\nAnalyze CV Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json().get("candidate_id")

def test_match_candidate(job_id, candidate_id):
    url = f"{BASE_URL}/match-candidate"
    params = {
        "job_id": job_id,
        "candidate_id": candidate_id
    }
    response = requests.post(url, params=params)
    print("\nMatch Candidate Response:")
    print(json.dumps(response.json(), indent=2))
    return response.json().get("match_id")

def test_schedule_interview(match_id):
    url = f"{BASE_URL}/schedule-interview/{match_id}"
    response = requests.post(url)
    print("\nSchedule Interview Response:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    print("Testing Job Screening AI API...")
    
    # Test analyze job
    job_id = test_analyze_job()
    
    # Test analyze CV (uncomment when you have a valid CV file)
    # candidate_id = test_analyze_cv()
    
    # Test match candidate (uncomment when you have both job_id and candidate_id)
    # match_id = test_match_candidate(job_id, candidate_id)
    
    # Test schedule interview (uncomment when you have a match_id)
    # test_schedule_interview(match_id) 