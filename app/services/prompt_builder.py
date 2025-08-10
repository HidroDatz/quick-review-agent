"""Build prompts for the code review model."""
from __future__ import annotations
from .template_parser import MRContext
import json


SYSTEM_PROMPT = (
    "You are a senior backend code reviewer for Python. Focus on correctness, "
    "security, reliability, performance, maintainability. Return ONLY valid JSON "
    "per schema. Prefer minimal, safe patches. Avoid duplicates. Treat lines prefixed [VI] as Vietnamese already translated to English."
)


def build_prompt(ctx: MRContext, diff_chunk: str) -> dict:
    meta_json = json.dumps(ctx.meta, ensure_ascii=False)
    user_prompt = (
        f"MR Meta: {meta_json}\n"
        f"Summary: {ctx.summary}\n"
        f"Implementation: {ctx.implementation}\n"
        f"Testing: {ctx.testing}\n"
        f"Security/Performance: {ctx.secperf}\n"
        f"Reviewer Hints: {ctx.hints}\n"
        f"Languages focus: {ctx.languages}\n\n"
        f"Unified diff hunk:\n{diff_chunk}\n\n"
        "Return JSON exactly in this schema:\n"
        "{\n  \"findings\": [\n    {\n      \"file\": \"str\",\n      \"start_line\": 0,\n      \"end_line\": 0,\n      \"severity\": \"critical|high|medium|low\",\n      \"category\": \"correctness|security|reliability|performance|api|testing|maintainability|style\",\n      \"rule_id\": \"PY.SEC.HTTP_NO_TIMEOUT\",\n      \"rule_version\": \"1.0.0\",\n      \"title\": \"short\",\n      \"rationale\": \"concise why\",\n      \"recommendation\": \"actionable fix\",\n      \"patch\": \"valid unified diff or empty\"\n    }\n  ],\n  \"confidence\": 0.0\n}"
    )
    return {"system": SYSTEM_PROMPT, "user": user_prompt}
