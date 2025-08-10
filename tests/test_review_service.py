import pytest

from app.services import review_service, gitlab_client
from app.utils.json_validator import ModelResponse, Finding


class DummyCompletions:
    def __init__(self, responses):
        self._responses = responses
        self._idx = 0

    async def create(self, **kwargs):
        content = self._responses[self._idx]
        self._idx += 1
        class Msg:
            def __init__(self, c):
                self.content = c
        class Choice:
            def __init__(self, c):
                self.message = Msg(c)
        class Resp:
            def __init__(self, c):
                self.choices = [Choice(c)]
        return Resp(content)


class DummyChat:
    def __init__(self, responses):
        self.completions = DummyCompletions(responses)


class DummyClient:
    def __init__(self, responses):
        self.chat = DummyChat(responses)


@pytest.mark.asyncio
async def test_call_model_retries_on_invalid_json():
    responses = ["not json", '{"findings": [], "confidence": 0.5}']
    client = DummyClient(responses)
    result = await review_service.call_model("sys", "user", client=client)
    assert result.confidence == 0.5


@pytest.mark.asyncio
async def test_trigger_review_stores_findings(monkeypatch):
    async def fake_get_merge_request(project_id, mr_iid):
        return {
            "description": "---\n"
            "type: feature\n"
            "scope: backend\n"
            "languages: [python]\n"
            "risk_level: low\n"
            "breaking_changes: false\n"
            "related_issue: ''\n"
            "---\n# Summary\nExample\n"
            "# Implementation Details\nDetails\n"
            "# Testing Plan\nTests\n"
            "# Security & Performance\nNone\n"
            "# Reviewer Hints\nN/A"
        }

    async def fake_get_changes(project_id, mr_iid):
        return {"changes": [{"diff": "@@\n+print('hi')\n"}]}

    async def fake_call_model(system_prompt, user_prompt, client=None):
        finding = Finding(
            file="a.py",
            start_line=1,
            end_line=1,
            severity="low",
            category="style",
            rule_id="PY.STYLE.TEST",
            rule_version="1.0.0",
            title="test",
            rationale="why",
            recommendation="fix",
            patch="",
        )
        return ModelResponse(findings=[finding], confidence=0.9)

    monkeypatch.setattr(review_service, "call_model", fake_call_model)
    monkeypatch.setattr(gitlab_client, "get_merge_request", fake_get_merge_request)
    monkeypatch.setattr(gitlab_client, "get_changes", fake_get_changes)

    await review_service.trigger_review(1, 2)
    findings = await review_service.get_current_findings(1, 2)
    assert findings and findings[0]["file"] == "a.py"
