from app.services.template_parser import parse_description
from app.services.prompt_builder import build_prompt

DESC = """---\ntype: feature\nscope: backend\nlanguages: [python]\nrisk_level: low\nbreaking_changes: false\nrelated_issue: ''\n---\n# Summary\nHi\n# Implementation Details\nImpl\n# Testing Plan\nTests\n# Security & Performance\nNone\n# Reviewer Hints\nN/A\n"""

def test_prompt_builder_contains_diff():
    ctx = parse_description(DESC)
    diff = "@@\n+print('a')\n"
    prompts = build_prompt(ctx, diff)
    assert "print('a')" in prompts["user"]
    assert "You are a senior backend" in prompts["system"]
