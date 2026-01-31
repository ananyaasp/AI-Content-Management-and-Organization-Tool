# AI-Powered Content Management and Organization Tool


## 📋 Project Description

An intelligent document and media organizer that automatically categorizes files, extracts metadata, and provides smart search capabilities using natural language processing. The project combines file system operations, text processing, and basic AI implementation for content analysis.

This repository contains the source code and documentation for the AI-Powered Content Management and Organization Tool project, developed as part of the UE23CS341A course at PES University.


## 🚀 Getting Started

### Prerequisites
1. System Requirements:
- Operating System: Windows 10 / 11, Ubuntu 22.04, or macOS
- Processor: Minimum 4 cores
- Memory: Minimum 8 GB RAM
- Disk Space: 2 GB (for embeddings, logs, and temp files)

2. Software Requirements:
- Python 3.10+ – Required for backend (FastAPI & ML libraries)
- pip (Python package manager) – For installing dependencies
- Node.js & npm (optional) – Only if any JS tools are used for visualization
- Git – For version control and cloning the repository
- Docker (optional) – If running inside a container
- FAISS (CPU version) – For semantic vector search (auto-installed via requirements.txt)

3. Python Dependencies:
All dependencies are listed in backend/requirements.txt, including:
- fastapi – Web framework for backend APIs
- uvicorn – ASGI server for FastAPI
- streamlit – Frontend dashboard
- sentence-transformers – Embedding generation
- faiss-cpu – Semantic similarity search
- pytest, pytest-cov – Testing and coverage
- python-jose, passlib – JWT authentication and password hashing
Install them with:
```bash
cd backend
pip install -r requirements.txt
```

### Installation
1. Clone the repository
   ```bash
   git clone https://github.com/pestechnology/PESU_EC_CSE_A_P27_AI_Powered_Content_Management_and_Organization_Too_team-24.git
   cd PESU_EC_CSE_A_P27_AI_Powered_Content_Management_and_Organization_Too_team-24
   ```

2. Install dependencies
   cd backend
   pip install -r requirements.txt
   export FASTAPI_APP=app.main:app
   uvicorn app.main:app --reload --port 8000 

3. Run the application
   cd frontend
   npm install
   npm start

## 📁 Project Structure

```
PESU_EC_CSE_A_P27_AI_Powered_Content_Management_and_Organization_Too_team-24/
├── src/                 # Source code
├── docs/               # Documentation
├── tests/              # Test files
├── .github/            # GitHub workflows and templates
├── README.md          # This file
└── ...
```

## ⚙️ CI/CD Pipeline
## What the Pipeline Does
- Automatically runs tests, linting, and build checks on every push or pull request.
- Ensures backend (FastAPI) dependencies install correctly and the app builds without errors.
- Verifies that all test cases pass before merging to the develop or main branch.
- Tracks test history and build success rates via GitHub Actions dashboard.

## Tools & Thresholds
- pytest – Runs backend unit and integration tests.
→ Threshold: All tests must pass (100% success expected before merge).
- pytest-cov – Measures backend test coverage.
→ Threshold: Minimum 80% code coverage required.
- lint – Performs static code analysis and style checks.
→ Threshold: No critical linting errors allowed.
- GitHub Actions – Automates CI/CD workflows (build, test, lint).
→ Threshold: Maintain at least 90% successful build rate across last 15 runs.

## 💻 Local Run Instructions
## 1. Backend (FastAPI):
```bash
cd backend
pip install -r requirements.txt
pytest --cov=app --cov-report=term-missing
uvicorn app.main:app --reload --port 8000
```
Backend API will be available at:
 http://127.0.0.1:8000
## 2. Frontend (Streamlit):
```bash
cd frontend
pip install streamlit requests
streamlit run app.py
```
The Streamlit dashboard will open in your browser at:
 http://localhost:8501

## 🧪 Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage
```



