# Quick Review Agent

Backend service for AI-powered GitLab merge request reviews.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables
See `.env.example` for required variables.

## Tests

```bash
pytest --cov=app
```

## Docker

```
docker-compose up --build
```
