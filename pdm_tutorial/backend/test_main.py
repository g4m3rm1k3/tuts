from fastapi.testclient import TestClient
from backend.app.main import app

# Create a test client
client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': "Hello from the PMD Backend"}


def test_get_files():
    """Test teh files list endpoint"""
    response = client.get("/api/files")
    assert response.status_code == 200
    data = response.json()
    assert "files" in data
    assert len(data["files"]) > 0


def test_get_file_not_found():
    """Test 404 for non-existent file"""
    response = client.get("/api/files/NONEXISTENT.mcam")
    assert response.status_code == 404


def test_checkout_file():
    """Test chckout endpoint"""
    response = client.post(
        "/api/checkout",
        json={
            "filename": "PN1001_OP1.mcam",
            "user": "mmclean",
            "message": "Testing checkout"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
