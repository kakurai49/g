from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.settings import reset_settings_cache


@pytest.fixture(autouse=True)
def reset_settings(monkeypatch: pytest.MonkeyPatch):
    for key in ["GIT_SHA", "BUILD_TIME", "APP_ENV", "PORT"]:
        monkeypatch.delenv(key, raising=False)
    reset_settings_cache()
    yield
    reset_settings_cache()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
