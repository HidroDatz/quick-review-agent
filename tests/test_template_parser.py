from app.services.template_parser import parse_description

SAMPLE = """---\ntype: feature\nscope: backend\nlanguages: [python]\nrisk_level: low\nbreaking_changes: false\nrelated_issue: ''\n---\n# Summary\nHello\n\n[VI] Xin chao\n# Implementation Details\nImpl\n# Testing Plan\nTests\n# Security & Performance\nNone\n# Reviewer Hints\nN/A\n"""

def test_parse_description():
    ctx = parse_description(SAMPLE)
    assert ctx.meta["type"] == "feature"
    assert "Xin chao" in ctx.summary
    assert ctx.languages == ["python"]
