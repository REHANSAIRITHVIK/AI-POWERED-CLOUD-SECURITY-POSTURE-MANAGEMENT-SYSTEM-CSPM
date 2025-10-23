# models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

class Resource(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cloud_provider: str
    resource_type: str
    resource_id: str
    config_json: str  # store JSON as string
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Finding(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    resource_id_ref: int
    title: str
    description: str
    severity: Severity
    risk_score: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    remedied: bool = False
