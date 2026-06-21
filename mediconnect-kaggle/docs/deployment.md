# Deployment Guide

## Local Development

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/mediconnect-agents.git
cd mediconnect-agents

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scriptsctivate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env with your GOOGLE_API_KEY

# 5. Run with ADK CLI
adk run agents/orchestrator

# 6. Or run web UI
adk web --host 0.0.0.0 --port 8000
```

## Docker Deployment

```bash
# Build and run locally
docker build -t mediconnect -f deployment/Dockerfile .
docker run -p 8000:8000 --env-file .env mediconnect

# Test health endpoint
curl http://localhost:8000/health
```

## Google Cloud Run Deployment

```bash
# One-click deploy
cd deployment
bash deploy.sh

# Or manual steps:
# 1. Build
gcloud builds submit --tag gcr.io/PROJECT_ID/mediconnect

# 2. Deploy
gcloud run deploy mediconnect   --image gcr.io/PROJECT_ID/mediconnect   --region us-central1   --allow-unauthenticated
```

## Kaggle Notebook

Upload the folder as a Kaggle Dataset, then open `kaggle_notebook.ipynb`.

## Required Environment Variables

| Variable | Source | Purpose |
|----------|--------|---------|
| GOOGLE_API_KEY | Google AI Studio | LLM access |
| ENCRYPTION_KEY | Generate with Fernet | Data encryption |
| PROJECT_ID | GCP Console | Cloud deployment |
