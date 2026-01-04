from __future__ import annotations


def test_dev_portal_renders_with_scripts(client):
    response = client.get("/dev")
    assert response.status_code == 200
    body = response.text

    assert "Dev Portal" in body
    assert "fetch('/health')" in body
    assert "fetch('/version')" in body
    assert "id=\"health\"" in body
    assert "id=\"version\"" in body
    assert "request failed" in body or "request failed".title() in body


def test_root_redirects_to_dev(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code in {302, 307, 308}
    assert response.headers["location"] == "/dev"
