"""Service orchestrating code reviews."""
from __future__ import annotations
import json
from typing import Dict, Tuple, List
from .template_parser import parse_description
from .diff_chunker import chunk_diff
from .prompt_builder import build_prompt
from ..utils.json_validator import validate_json
from .dedupe import dedupe_key

FINDINGS_STORE: Dict[Tuple[int, int], List[dict]] = {}


async def call_model(system_prompt: str, user_prompt: str) -> dict:
    """Stub model call returning empty findings."""
    # In production, call Qwen-Coder here.
    return {"findings": [], "confidence": 1.0}


async def trigger_review(project_id: int, mr_iid: int) -> None:
    """Run review for given MR (simplified)."""
    # Normally, fetch MR description and changes via GitLab API.
    # Here, we use placeholders for tests.
    description = """---\ntype: feature\nscope: backend\nlanguages: [python]\nrisk_level: low\nbreaking_changes: false\nrelated_issue: ''\n---\n# Summary\nExample\n# Implementation Details\nDetails\n# Testing Plan\nTests\n# Security & Performance\nNone\n# Reviewer Hints\nN/A\n"""
    ctx = parse_description(description)
    diff = "@@\n+print('hi')\n"
    hunks = chunk_diff(diff)
    findings: List[dict] = []
    for hunk in hunks:
        prompts = build_prompt(ctx, hunk)
        resp = await call_model(prompts["system"], prompts["user"])
        data = validate_json(json.dumps(resp))
        for f in data.findings:
            key = dedupe_key(f.file, f.rule_id, f.title, f.start_line)
            findings.append({**f.model_dump(), "dedupe_key": key})
    FINDINGS_STORE[(project_id, mr_iid)] = findings


async def get_current_findings(project_id: int, mr_iid: int) -> List[dict]:
    return FINDINGS_STORE.get((project_id, mr_iid), [])
