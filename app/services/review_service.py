"""Service orchestrating code reviews."""
from __future__ import annotations

import json
from typing import Dict, Tuple, List

from openai import AsyncOpenAI
from pydantic import ValidationError

from .template_parser import parse_description
from .diff_chunker import chunk_diff
from .prompt_builder import build_prompt
from ..utils.json_validator import ModelResponse, validate_json
from .dedupe import dedupe_key
from ..config import settings


FINDINGS_STORE: Dict[Tuple[int, int], List[dict]] = {}


async def call_model(
    system_prompt: str,
    user_prompt: str,
    *,
    client: AsyncOpenAI | None = None,
) -> ModelResponse:
    """Call OpenAI model and return validated JSON response.

    Retries once if the model response fails validation.
    """

    client = client or AsyncOpenAI(
        api_key=settings.openai_api_key, base_url=settings.openai_base_url
    )

    for _ in range(2):  # initial try + one retry
        response = await client.chat.completions.create(
            model=settings.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content or "{}"
        try:
            return validate_json(content)
        except (json.JSONDecodeError, ValidationError):
            continue

    return ModelResponse(findings=[], confidence=0.0)


async def trigger_review(project_id: int, mr_iid: int) -> None:
    """Run review for a given Merge Request."""

    from . import gitlab_client

    mr = await gitlab_client.get_merge_request(project_id, mr_iid)
    changes = await gitlab_client.get_changes(project_id, mr_iid)

    ctx = parse_description(mr.get("description", ""))
    findings: List[dict] = []

    for change in changes.get("changes", []):
        hunks = chunk_diff(change.get("diff", ""))
        for hunk in hunks:
            prompts = build_prompt(ctx, hunk)
            data = await call_model(prompts["system"], prompts["user"])
            for f in data.findings:
                key = dedupe_key(f.file, f.rule_id, f.title, f.start_line)
                findings.append({**f.model_dump(), "dedupe_key": key})

    if findings:
        lines = [
            f"- {f['severity'].upper()}: {f['file']}:{f['start_line']} {f['title']}"
            for f in findings
        ]
        summary = "AI Review Findings:\n" + "\n".join(lines)
    else:
        summary = "AI Review: no issues found."

    await gitlab_client.post_comment(project_id, mr_iid, summary)
    FINDINGS_STORE[(project_id, mr_iid)] = findings


async def get_current_findings(project_id: int, mr_iid: int) -> List[dict]:
    return FINDINGS_STORE.get((project_id, mr_iid), [])
