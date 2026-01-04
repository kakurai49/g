from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Mapping, MutableMapping


@dataclass
class Settings:
    """Application settings loaded from environment variables."""

    service: str = "g"
    port: int = 8080
    git_sha: str = "unknown"
    build_time: str | None = None
    app_env: str = "dev"

    @classmethod
    def from_env(
        cls, environ: Mapping[str, str] | MutableMapping[str, str] | None = None
    ) -> "Settings":
        env = environ or os.environ
        return cls(
            service="g",
            port=int(env.get("PORT", 8080)),
            git_sha=env.get("GIT_SHA", "unknown"),
            build_time=env.get("BUILD_TIME"),
            app_env=env.get("APP_ENV", "dev"),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
