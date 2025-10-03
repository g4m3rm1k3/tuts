from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_get_files_returns_array():
    response = client.get("/api/files")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3
