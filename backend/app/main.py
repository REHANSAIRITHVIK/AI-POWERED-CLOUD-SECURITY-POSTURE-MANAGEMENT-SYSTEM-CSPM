# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from .db import init_db, get_session
from .models import Resource, Finding, Severity
from .schemas import ResourceIn, FindingOut
from .ai_detector import AIDetector
from .sample_data import SAMPLE_RESOURCES
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import cloud_routes  # make sure routes/cloud_routes.py exists

# ✅ Initialize FastAPI App with proper arguments for Python 3.11+
app = FastAPI(
    title="AI CSPM API",
    description="AI Powered Cloud Security Posture Management System Backend",
    version="1.0.0"
)

# ✅ Enable CORS so your frontend can access the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include your routes
app.include_router(cloud_routes.router, prefix="/api/cloud", tags=["Cloud CSPM"])

# ✅ Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the AI-Powered CSPM API!"}

# ✅ For debugging or health check
@app.get("/health")
def health_check():
    return {"status": "running", "version": "1.0.0"}

# ✅ Run server (only when directly executed)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)


