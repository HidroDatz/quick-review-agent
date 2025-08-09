from __future__ import annotations
from pydantic import BaseModel
from typing import Dict, List


class MRContextSchema(BaseModel):
    meta: Dict[str, str]
    summary: str
    implementation: str
    testing: str
    secperf: str
    hints: str
    languages: List[str]
