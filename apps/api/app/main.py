import os
from datetime import datetime, timezone
from typing import Dict

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

SERVICE_NAME = "g"


def get_version() -> str:
    return os.getenv("GIT_SHA", "unknown")


def build_health_response() -> Dict[str, str]:
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "version": get_version(),
        "time": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/health")
def health() -> Dict[str, str]:
    return build_health_response()


@app.get("/version")
def version() -> Dict[str, str]:
    return {"version": get_version()}


@app.get("/dev", response_class=HTMLResponse)
def dev() -> HTMLResponse:
    version = get_version()
    html_content = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <title>Dev Portal</title>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; padding: 1.5rem; }}
            pre {{ background: #f4f4f5; padding: 1rem; border-radius: 8px; overflow: auto; }}
            .version {{ margin-top: 0.5rem; color: #555; }}
        </style>
    </head>
    <body>
        <h1>Dev Portal</h1>
        <p class=\"version\">Version: {version}</p>
        <div id=\"health\">Loading health...</div>
        <script>
            async function loadHealth() {{
                const container = document.getElementById('health');
                try {{
                    const response = await fetch('/health');
                    const data = await response.json();
                    container.innerHTML = '<h2>Health</h2><pre>' + JSON.stringify(data, null, 2) + '</pre>';
                }} catch (error) {{
                    container.innerHTML = '<p style="color:red;">Failed to load health</p>';
                }}
            }}
            loadHealth();
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
