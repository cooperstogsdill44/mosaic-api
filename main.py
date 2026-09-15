from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from exposure_score import score_profile

app = FastAPI(title="Mosaic API")

# Allows your Vercel site to call this API from the browser
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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