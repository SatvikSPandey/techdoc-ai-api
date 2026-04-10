# TechDoc AI API

A production-grade REST API for AI-powered technical document analysis. Built with FastAPI, deployed on AWS EC2 with Docker and GitHub Actions CI/CD.

## Live Demo

**Base URL:** http://13.201.68.108:8000

**Interactive API Docs:** http://13.201.68.108:8000/docs

**Health Check:** http://13.201.68.108:8000/api/v1/health

**Metrics:** http://13.201.68.108:8000/api/v1/metrics

> For a demo API key to test the AI endpoints, contact: satvikpan@gmail.com

## What It Does

- **Document Summarization** — Upload any engineering or technical document and get a structured summary with 5 extracted key points
- **Document Q&A** — Ask questions about a document and get AI-powered answers with confidence scores

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python) |
| AI Engine | Cohere command-r-08-2024 |
| Container | Docker |
| Cloud | AWS EC2 (Mumbai region) |
| CI/CD | GitHub Actions |
| Auth | API Key (X-API-Key header) |
| Rate Limiting | 10 requests/minute per IP |

## API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | /api/v1/health | No | Health check and uptime |
| GET | /api/v1/metrics | No | Request counts and performance |
| POST | /api/v1/summarize | Yes | Summarize a technical document |
| POST | /api/v1/ask | Yes | Ask a question about a document |

## Architecture

Developer → GitHub → GitHub Actions → AWS EC2
↓
Docker Container
↓
FastAPI App
↓
Cohere AI API


## How to Run Locally

```bash
# Clone the repo
git clone https://github.com/SatvikSPandey/techdoc-ai-api.git
cd techdoc-ai-api

# Create virtual environment
py -3.11 -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Add your COHERE_API_KEY to .env

# Run the server
uvicorn app.main:app --reload --port 8000
```

## CI/CD Pipeline

Every push to `main` branch automatically:
1. Runs on GitHub Actions
2. SSHs into AWS EC2
3. Pulls latest code
4. Rebuilds Docker image
5. Restarts the container

## Project Structure

techdoc-ai-api/
├── app/
│   ├── api/routes/          # FastAPI route handlers
│   ├── core/                # Config, auth, rate limiting
│   ├── models/              # Pydantic schemas
│   ├── services/            # AI backend abstraction
│   └── utils/               # Logging, metrics, prompts
├── .github/workflows/       # GitHub Actions CI/CD
├── Dockerfile
├── docker-compose.yml
└── requirements.txt

## Author

**Satvik Pandey** — AI Engineer | Python Developer | LLM Systems

[LinkedIn](https://www.linkedin.com/in/satvikpandey-433555365) | [GitHub](https://github.com/SatvikSPandey)