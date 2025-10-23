from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
import random

router = APIRouter()

# ---------------------------------------------------------------------
# 📦 MODELS
# ---------------------------------------------------------------------
class CloudAsset(BaseModel):
    service: str
    issue: str
    risk: str


class CloudScanRequest(BaseModel):
    provider: str  # "AWS", "Azure", "GCP"


# ---------------------------------------------------------------------
# ⚙️ MOCK DATABASE / AI LOGIC
# ---------------------------------------------------------------------
MOCK_ASSETS = {
    "AWS": [
        {"service": "S3", "issue": "Public bucket without encryption", "risk": "High"},
        {"service": "EC2", "issue": "Outdated AMI version", "risk": "Medium"},
        {"service": "IAM", "issue": "Root access key active", "risk": "Critical"},
    ],
    "Azure": [
        {"service": "VM", "issue": "Open port 22 detected", "risk": "Medium"},
        {"service": "Storage", "issue": "Unencrypted blob storage", "risk": "High"},
        {"service": "KeyVault", "issue": "Key rotation overdue", "risk": "Low"},
    ],
    "GCP": [
        {"service": "Compute", "issue": "Default network in use", "risk": "Medium"},
        {"service": "Storage", "issue": "IAM policy too permissive", "risk": "High"},
        {"service": "BigQuery", "issue": "Dataset public access", "risk": "Critical"},
    ],
}


def ai_risk_score(issue: str, risk: str) -> float:
    """
    Mock AI risk evaluation model.
    Returns a floating risk score between 0 and 1.
    """
    base = {"Low": 0.2, "Medium": 0.5, "High": 0.8, "Critical": 0.95}
    noise = random.uniform(-0.05, 0.05)
    return max(0, min(1, base.get(risk, 0.4) + noise))


# ---------------------------------------------------------------------
# 🚀 ROUTES
# ---------------------------------------------------------------------
@router.post("/scan", response_model=List[CloudAsset])
async def scan_cloud_assets(request: CloudScanRequest):
    """
    Simulates a cloud configuration scan and AI-based analysis.
    """
    provider = request.provider.capitalize()

    if provider not in MOCK_ASSETS:
        raise HTTPException(status_code=400, detail="Unsupported cloud provider")

    results = []
    for asset in MOCK_ASSETS[provider]:
        score = ai_risk_score(asset["issue"], asset["risk"])
        results.append({
            "service": asset["service"],
            "issue": asset["issue"],
            "risk": f"{asset['risk']} ({score:.2f})"
        })

    return results


@router.get("/providers")
async def get_supported_providers():
    """Returns list of supported cloud platforms."""
    return {"providers": list(MOCK_ASSETS.keys())}


@router.get("/summary")
async def get_summary():
    """Returns overall summary of system risks (mock data)."""
    summary = {
        "total_assets": sum(len(v) for v in MOCK_ASSETS.values()),
        "high_risk": random.randint(2, 5),
        "medium_risk": random.randint(3, 6),
        "low_risk": random.randint(1, 4),
    }
    return {"summary": summary}
