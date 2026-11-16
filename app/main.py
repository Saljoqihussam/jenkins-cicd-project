
from fastapi import FastAPI

app = FastAPI(
    title="Student Management API",
    description="A sample API for our Jenkins CI/CD project",
    version="1.0.0"
)

students = [
    {"id": 1, "name": "Ali", "department": "Computer Science"},
    {"id": 2, "name": "Ahmed", "department": "Software Engineering"},
    {"id": 3, "name": "Sara", "department": "Artificial Intelligence"}
]


@app.get("/")
def home():
    return {
        "message": "Welcome to Student Management API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/students")
def get_students():
    return {
        "total": len(students),
        "students": students
    }
