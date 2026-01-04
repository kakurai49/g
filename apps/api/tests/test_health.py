from __future__ import annotations

from datetime import datetime

from app.settings import reset_settings_cache


def test_health_returns_status_and_checks(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "g"
    assert data["checks"]["app"] == "ok"
    assert data["version"] == "unknown"

    parsed_time = datetime.fromisoformat(data["time"])
    assert parsed_time.tzinfo is not None


def test_health_uses_git_sha_from_env(client, monkeypatch):
    monkeypatch.setenv("GIT_SHA", "abc123")
    reset_settings_cache()

    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["version"] == "abc123"
