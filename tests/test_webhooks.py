from fastapi.testclient import TestClient
from app.main import app
from app.config import settings


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
