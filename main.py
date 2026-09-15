"""
main.py

A minimal FastAPI backend exposing the exposure-scoring logic
as a real API endpoint. Run with:
    uvicorn main:app --reload
Then test with:
    curl -X POST http://127.0.0.1:8000/scan -H "Content-Type: application/json" -d "{\"username_reused_count\": 2, \"school_public\": true, \"location_public\": true, \"connection_count\": 3}"
"""

from fastapi import FastAPI
from pydantic import BaseModel
from exposure_score import score_profile

app = FastAPI(title="Mosaic API")


class ProfileInput(BaseModel):
    username_reused_count: int = 0
    school_public: bool = False
    location_public: bool = False
    connection_count: int = 0


@app.get("/")
def root():
    return {"status": "Mosaic API is running"}


@app.post("/scan")
def scan(profile: ProfileInput):
    result = score_profile(profile.model_dump())
    return result
