# AI-Powered Job Screening System

A state-of-the-art multi-agent system for automated job screening and candidate matching.

## Features

- 🤖 Multi-agent architecture for intelligent job screening
- 📊 Advanced CV parsing and analysis
- 🎯 Smart job-candidate matching using embeddings
- 📧 Automated interview scheduling
- 📈 Performance analytics and insights

## System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  JD Analyzer    │     │   CV Analyzer   │     │    Matcher      │
│     Agent       │────▶│     Agent       │────▶│     Agent       │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                       │
         ▼                      ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Job Database   │     │  CV Database    │     │  Match Database │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                      │                       │
         ▼                      ▼                       ▼
┌─────────────────────────────────────────────────────────┐
│                    Scheduler Agent                      │
└─────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Email Service  │
                    └─────────────────┘
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama:
- Windows: Download from https://ollama.com
- Mac/Linux: `curl -fsSL https://ollama.com/install.sh | sh`

3. Pull the model:
```bash
ollama pull mistral
```

4. Run the application:
```bash
python src/main.py
```

## Project Structure

```
job-screening-ai/
├── src/
│   ├── agents/           # Multi-agent system
│   ├── data_processing/  # Data processing modules
│   ├── database/         # Database models and operations
│   └── utils/           # Utility functions
├── data/
│   ├── raw/            # Original dataset
│   ├── processed/      # Processed data
│   └── embeddings/     # Generated embeddings
├── tests/              # Test cases
└── config/            # Configuration files
```

## Key Components

1. **JD Analyzer Agent**
   - Parses job descriptions
   - Extracts key requirements
   - Generates job embeddings

2. **CV Analyzer Agent**
   - Processes CV documents
   - Extracts candidate information
   - Generates candidate embeddings

3. **Matcher Agent**
   - Calculates job-candidate compatibility
   - Ranks candidates by match score
   - Generates matching reports

4. **Scheduler Agent**
   - Manages interview scheduling
   - Sends automated emails
   - Tracks interview status

## Technologies Used

- **AI/ML**: Ollama, Sentence Transformers
- **Backend**: FastAPI, SQLAlchemy
- **Database**: SQLite
- **Processing**: Pandas, NumPy
- **Document Processing**: PyPDF2, python-docx

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 