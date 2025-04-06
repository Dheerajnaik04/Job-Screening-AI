# AI-Powered Job Screening System

A multi-agent AI system that automates the recruitment process by analyzing job descriptions, matching candidate qualifications, shortlisting candidates, and scheduling interviews.

## Features

- **Job Description Analysis**: Extract key information from job descriptions using AI
- **CV Analysis**: Parse and analyze CVs to extract candidate information
- **Smart Matching**: Match candidates with jobs using multiple criteria
- **Interview Scheduling**: Automatically schedule and manage interviews
- **Database Management**: Store and manage all recruitment data

## Architecture

The system consists of four main agents:

1. **JD Analyzer Agent**: Analyzes job descriptions and extracts key information
2. **CV Analyzer Agent**: Processes CVs and extracts candidate information
3. **Matcher Agent**: Matches candidates with jobs based on multiple criteria
4. **Scheduler Agent**: Manages interview scheduling and communication

## Technical Stack

- **Python 3.9+**
- **FastAPI**: Web framework for building APIs
- **SQLAlchemy**: Database ORM
- **Sentence Transformers**: For semantic similarity
- **Ollama**: For natural language understanding
- **SQLite**: Database

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama:
- Windows: Download from https://ollama.com
- Mac/Linux: `curl -fsSL https://ollama.com/install.sh | sh`

3. Pull the required model:
```bash
ollama pull mistral
```

4. Run the application:
```bash
python src/main.py
```

## API Endpoints

### Job Management
- `POST /analyze-job`: Submit a job description for analysis
- `GET /job-matches/{job_id}`: View matches for a job

### Candidate Management
- `POST /analyze-cv`: Upload and analyze a CV
- `GET /candidate-matches/{candidate_id}`: View matches for a candidate

### Matching
- `POST /match-candidate`: Match a candidate with a job

## Project Structure

```
job-screening-ai/
├── src/
│   ├── agents/
│   │   ├── jd_analyzer.py
│   │   ├── cv_analyzer.py
│   │   ├── matcher.py
│   │   └── scheduler.py
│   ├── database/
│   │   ├── models.py
│   │   └── db_manager.py
│   ├── data_processing/
│   │   └── ...
│   └── utils/
│       └── ...
├── data/
│   ├── raw/
│   ├── processed/
│   └── embeddings/
├── tests/
├── config/
└── requirements.txt
```

## Database Schema

### Jobs
- id: Integer (Primary Key)
- title: String
- description: String
- required_skills: JSON
- preferred_skills: JSON
- experience: String
- education: String
- responsibilities: JSON
- embedding: JSON
- created_at: DateTime

### Candidates
- id: Integer (Primary Key)
- name: String
- email: String
- phone: String
- skills: JSON
- experience: JSON
- education: JSON
- embedding: JSON
- created_at: DateTime

### Matches
- id: Integer (Primary Key)
- job_id: Integer (Foreign Key)
- candidate_id: Integer (Foreign Key)
- match_score: Float
- match_details: JSON
- status: String
- created_at: DateTime

### Interviews
- id: Integer (Primary Key)
- match_id: Integer (Foreign Key)
- date: DateTime
- duration: Integer
- type: String
- format: String
- topics: JSON
- interviewers: JSON
- status: String
- created_at: DateTime

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 