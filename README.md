# Jenkins CI/CD Pipeline Demo

A Student Management REST API built using FastAPI, with a full Jenkins CI/CD pipeline:
**GitHub → Jenkins → Pytest → Docker → Docker Hub → Kubernetes**.

## Features

- Home endpoint
- Health check endpoint
- Student information endpoint
- Automated tests using Pytest
- Automated build, test, push and deploy with Jenkins

## Technologies

- Python 3.12
- FastAPI
- Uvicorn
- Pytest
- Docker
- Jenkins
- Kubernetes

## Project structure

```
app/                 FastAPI application (main.py)
tests/               Pytest tests
k8s/deployment.yaml  Kubernetes Deployment (2 replicas, health probes)
k8s/service.yaml     Kubernetes NodePort Service (port 30080)
Dockerfile           Image for the API
Dockerfile.jenkins   Jenkins image with Docker CLI + kubectl
Jenkinsfile          Pipeline as Code
```

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

## CI/CD Pipeline

| Stage | What it does |
|---|---|
| Checkout | Pulls the latest commit from GitHub |
| Install Dependencies & Test | Installs requirements and runs Pytest inside a `python:3.12-slim` container |
| Build Docker Image | Builds `hussam160803/jenkins-cicd-api:<build number>` and `:latest` |
| Push to Docker Hub | Logs in with Jenkins credentials and pushes both tags |
| Deploy to Kubernetes | Applies `k8s/` manifests with the new tag and waits for the rollout |
| Notify | Prints success/failure with build details in the console |

The pipeline is triggered automatically by new commits (`pollSCM` every ~2 minutes).

## Jenkins setup

1. Build and run Jenkins:

```bash
docker build -t jenkins-cicd -f Dockerfile.jenkins .
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  -v /var/run/docker.sock:/var/run/docker.sock \
  --add-host kubernetes.docker.internal:host-gateway \
  jenkins-cicd
```

2. Add credentials in **Manage Jenkins → Credentials**:
   - `dockerhub-credentials` — Username with password (Docker Hub)
   - `kubeconfig` — Secret file (your `~/.kube/config`)
3. Create a **Pipeline** job → "Pipeline script from SCM" → Git → this repo URL → Script Path `Jenkinsfile`.

## Access the deployed app

```bash
kubectl get pods,svc -l app=student-api
```

- Docker Desktop Kubernetes: http://localhost:30080
- Minikube: `minikube service student-api --url`
