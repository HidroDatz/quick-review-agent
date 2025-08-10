from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.routers import webhooks
import pytest


def test_webhook_rejects_invalid_token():
    original = settings.webhook_secret
    settings.webhook_secret = "secret"
    client = TestClient(app)
    try:
        response = client.post("/gitlab/webhook", json={})
        assert response.status_code == 401
        response = client.post(
            "/gitlab/webhook", json={}, headers={"X-Gitlab-Token": "wrong"}
        )
        assert response.status_code == 401
    finally:
        settings.webhook_secret = original


@pytest.mark.parametrize("action", ["open", "update"])
def test_merge_request_actions_trigger_review(monkeypatch, action):
    original = settings.webhook_secret
    settings.webhook_secret = "secret"
    called = []

    async def fake_trigger_review(project_id, mr_iid):
        called.append((project_id, mr_iid))

    monkeypatch.setattr(webhooks, "trigger_review", fake_trigger_review)
    client = TestClient(app)
    try:
        payload = {
            "object_kind": "merge_request",
            "project": {"id": 1},
            "object_attributes": {"iid": 2, "action": action},
        }
        response = client.post(
            "/gitlab/webhook",
            json=payload,
            headers={"X-Gitlab-Token": "secret"},
        )
        assert response.status_code == 200
        assert called == [(1, 2)]
    finally:
        settings.webhook_secret = original
