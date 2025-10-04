from app.main import app
from fastapi.testclient import TestClient
import tempfile


client = TestClient(app)


def test_get_files_from_real_dir(tmp_path):
    # Create temp dir with mock files
    mock_repo = tmp_path / "repo"
    mock_repo.mkdir()
    (mock_repo / "test.mcam").touch()
    app.state.repo_path = str(mock_repo)  # Override for test

    response = client.get("/api/files")
    assert len(response.json()) == 3
    assert "1801811.mcam" in [f["name"] for f in response.json()]


def test_serves_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_get_files_returns_array():
    response = client.get("/api/files")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 3


def test_integration_with_css():
    response = client.get("/")
    assert "/static/css/style.css" in response.text  # Verifies link in HTML
