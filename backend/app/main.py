import psycopg
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import test_connection

app = FastAPI(
    title="RagTrace API",
    description="AI-powered document research assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {"message": "RagTrace API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/health/db")
def database_health():
    try:
        version = test_connection()

        return {
            "status": "connected",
            "database": "PostgreSQL",
            "version": version
        }

    except psycopg.Error:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed."
        )