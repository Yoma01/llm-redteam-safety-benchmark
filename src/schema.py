from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime


class AttackSample(BaseModel):
    attack_id: str
    category: str
    subcategory: str
    attack_family: str
    base_intent: str
    rendered_prompt: Optional[str] = None
    multi_turn_context: Optional[List[str]] = None
    severity_target: int = Field(ge=0, le=4)


class ResponseRecord(BaseModel):
    run_id: str
    timestamp: str
    model_name: str
    defense_name: str
    attack_id: str
    category: str
    subcategory: str
    attack_family: str
    turn_number: int
    prompt: str
    response: str
    latency_seconds: float


class SafetyScore(BaseModel):
    run_id: str
    refusal_label: Literal["full_refusal", "partial_refusal", "no_refusal", "ambiguous"]
    compliance_label: Literal["harmful_compliance", "benign_compliance", "ambiguous"]
    severity_score: int = Field(ge=0, le=4)
    failure_mode: str
    confidence: float = Field(ge=0.0, le=1.0)
    judge_reasoning_summary: str


def now_iso() -> str:
    return datetime.utcnow().isoformat()
