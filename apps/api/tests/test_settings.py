from __future__ import annotations

from app.settings import Settings


def test_settings_defaults():
    settings = Settings.from_env({})

    assert settings.service == "g"
    assert settings.port == 8080
    assert settings.git_sha == "unknown"
    assert settings.build_time is None
    assert settings.app_env == "dev"


def test_settings_reads_environment():
    settings = Settings.from_env(
        {
            "PORT": "9090",
            "GIT_SHA": "sha-123",
            "BUILD_TIME": "2024-06-01T00:00:00Z",
            "APP_ENV": "prod",
        }
    )

    assert settings.port == 9090
    assert settings.git_sha == "sha-123"
    assert settings.build_time == "2024-06-01T00:00:00Z"
    assert settings.app_env == "prod"
