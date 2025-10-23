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
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI("AI CSPM API")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title,
        swagger_js_url="/static/swagger_custom.js"
    )



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize DB & AI
init_db()
detector = AIDetector()

@app.on_event("startup")
def seed_sample():
    sess = get_session()
    # seed only if no resources
    existing = sess.exec(select(Resource)).first()
    if existing is None:
        for r in SAMPLE_RESOURCES:
            res = Resource(
                cloud_provider=r["cloud_provider"],
                resource_type=r["resource_type"],
                resource_id=r["resource_id"],
                config_json=json.dumps(r["config"])
            )
            sess.add(res)
        sess.commit()
    sess.close()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/scan", response_model=list[FindingOut])
def scan_resources(resources: list[ResourceIn]):
    sess = get_session()
    created_findings = []
    for r in resources:
        res = Resource(
            cloud_provider=r.cloud_provider,
            resource_type=r.resource_type,
            resource_id=r.resource_id,
            config_json=json.dumps(r.config)
        )
        sess.add(res)
        sess.commit()
        # detect
        score = detector.score_config(r.config)
        explanation = detector.explain(r.config)
        # map score to severity
        if score >= 0.75:
            sev = Severity.HIGH
        elif score >= 0.4:
            sev = Severity.MEDIUM
        else:
            sev = Severity.LOW
        finding = Finding(
            resource_id_ref=res.id,
            title=f"Risky configuration for {r.resource_id}",
            description=explanation,
            severity=sev,
            risk_score=score,
        )
        sess.add(finding)
        sess.commit()
        created_findings.append(FindingOut(
            id=finding.id,
            resource_id_ref=finding.resource_id_ref,
            title=finding.title,
            description=finding.description,
            severity=finding.severity.value,
            risk_score=finding.risk_score,
            remedied=finding.remedied
        ))
    sess.close()
    return created_findings

@app.get("/findings", response_model=list[FindingOut])
def get_findings():
    sess = get_session()
    q = sess.exec(select(Finding).order_by(Finding.risk_score.desc()))
    out = []
    for f in q:
        out.append(FindingOut(
            id=f.id,
            resource_id_ref=f.resource_id_ref,
            title=f.title,
            description=f.description,
            severity=f.severity.value,
            risk_score=f.risk_score,
            remedied=f.remedied
        ))
    sess.close()
    return out

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is running successfully 🚀"}


@app.post("/remediate/{finding_id}", response_model=FindingOut)
def remediate(finding_id: int):
    sess = get_session()
    f = sess.get(Finding, finding_id)
    if not f:
        sess.close()
        raise HTTPException(status_code=404, detail="Finding not found")
    f.remedied = True
    sess.add(f)
    sess.commit()
    out = FindingOut(
        id=f.id,
        resource_id_ref=f.resource_id_ref,
        title=f.title,
        description=f.description,
        severity=f.severity.value,
        risk_score=f.risk_score,
        remedied=f.remedied
    )
    sess.close()
    return out
