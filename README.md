# Mosaic API

FastAPI backend for the Mosaic digital identity platform.

## Local setup
    python -m venv venv
    venv\Scripts\activate        (Windows)
    source venv/bin/activate     (Mac/Linux)
    pip install -r requirements.txt
    uvicorn main:app --reload

## Endpoints
- GET  /            health check
- POST /scan        submit a profile, get back an exposure score
