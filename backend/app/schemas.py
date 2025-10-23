# schemas.py
from pydantic import BaseModel
from typing import Any, Optional, List
from enum import Enum

class ResourceIn(BaseModel):
    cloud_provider: str
    resource_type: str
    resource_id: str
    config: dict

class FindingOut(BaseModel):
    id: int
    resource_id_ref: int
    title: str
    description: str
    severity: str
    risk_score: float
    remedied: bool
