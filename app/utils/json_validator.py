from pydantic import BaseModel, Field, ValidationError
from typing import List


class Finding(BaseModel):
    file: str
    start_line: int
    end_line: int
    severity: str
    category: str
    rule_id: str
    rule_version: str
    title: str
    rationale: str
    recommendation: str
    patch: str | None = ""


class ModelResponse(BaseModel):
    findings: List[Finding]
    confidence: float = Field(ge=0.0, le=1.0)


def validate_json(data: str) -> ModelResponse:
    """Validate model JSON output using Pydantic."""
    return ModelResponse.model_validate_json(data)
