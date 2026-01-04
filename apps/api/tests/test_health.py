import sys
from pathlib import Path

from fastapi.testclient import TestClient

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from app.main import app  # noqa: E402


client = TestClient(app)


def test_health_returns_status_ok():
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert "status" in payload


def test_dev_endpoint_serves_html():
    response = client.get("/dev")
    assert response.status_code == 200
    assert "Dev Portal" in response.text
