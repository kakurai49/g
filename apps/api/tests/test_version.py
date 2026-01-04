from __future__ import annotations

from app.settings import reset_settings_cache


def test_version_returns_service_and_version(client):
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()

    assert data["service"] == "g"
    assert data["version"] == "unknown"
    assert "build_time" not in data


def test_version_includes_env_values(client, monkeypatch):
    monkeypatch.setenv("GIT_SHA", "v1.2.3")
    monkeypatch.setenv("BUILD_TIME", "2024-01-01T00:00:00Z")
    reset_settings_cache()

    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()

    assert data["version"] == "v1.2.3"
    assert data["build_time"] == "2024-01-01T00:00:00Z"
