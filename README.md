
# Jenkins CI/CD Pipeline Demo

A Student Management REST API built using FastAPI.

## Features

- Home endpoint
- Health check endpoint
- Student information endpoint
- Automated tests using Pytest

## Technologies

- Python 3.12
- FastAPI
- Uvicorn
- Pytest
- Docker
- Jenkins
- Kubernetes

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Run tests:

```bash
pytest -v
```

## API Endpoints

- GET /
- GET /health
- GET /students
