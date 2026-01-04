from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, RedirectResponse

from app.settings import get_settings

app = FastAPI()


def _isoformat_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@app.get("/health")
def health() -> Dict[str, Any]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.service,
        "version": settings.git_sha,
        "time": _isoformat_now(),
        "checks": {"app": "ok"},
    }


@app.get("/version")
def version() -> Dict[str, Any]:
    settings = get_settings()
    payload: Dict[str, Any] = {"service": settings.service, "version": settings.git_sha}
    if settings.build_time:
        payload["build_time"] = settings.build_time
    return payload


@app.get("/dev", response_class=HTMLResponse)
def dev_portal() -> HTMLResponse:
    settings = get_settings()
    html_content = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>Dev Portal</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
                padding: 1.25rem;
            }}
            pre {{ background: #f4f4f5; padding: 1rem; border-radius: 8px; overflow: auto; }}
            .error {{ color: #b91c1c; font-weight: 600; }}
            .grid {{ display: grid; gap: 1rem; }}
            .card {{ border: 1px solid #e5e7eb; border-radius: 10px; padding: 1rem; }}
        </style>
    </head>
    <body>
        <h1>Dev Portal</h1>
        <p class=\"version\">Service: {settings.service} | Version: {settings.git_sha}</p>
        <div class=\"grid\">
            <div class=\"card\" id=\"health-card\">
                <h2>Health</h2>
                <div id=\"health\">Loading health...</div>
            </div>
            <div class=\"card\" id=\"version-card\">
                <h2>Version</h2>
                <div id=\"version\">Loading version...</div>
            </div>
            <div class=\"card\">
                <h2>Debug</h2>
                <p>Environment: {settings.app_env}</p>
                <p>PORT: {settings.port}</p>
            </div>
        </div>
        <script>
            // Dev Portal fetch targets: fetch('/health'), fetch('/version')
            const healthEndpoint = '/health';
            const versionEndpoint = '/version';

            async function fetchJson(path) {{
                const response = await fetch(path);
                if (!response.ok) throw new Error(`request failed: ${{path}}`);
                return response.json();
            }}

            async function loadHealth() {{
                const container = document.getElementById('health');
                try {{
                    const data = await fetchJson(healthEndpoint);
                    container.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                }} catch (error) {{
                    container.innerHTML = `<p class=\"error\">${{error.message}}</p>`;
                }}
            }}

            async function loadVersion() {{
                const container = document.getElementById('version');
                try {{
                    const data = await fetchJson(versionEndpoint);
                    container.innerHTML = '<pre>' + JSON.stringify(data, null, 2) + '</pre>';
                }} catch (error) {{
                    container.innerHTML = `<p class=\"error\">${{error.message}}</p>`;
                }}
            }}

            loadHealth();
            loadVersion();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/dev")
