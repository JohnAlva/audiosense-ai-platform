from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "AudioSense AI" in data["service"]

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"

def test_invalid_file_extension():
    response = client.post(
        "/api/v1/transcribe",
        files={"file": ("test.txt", b"plain text is not audio", "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported format" in response.json()["detail"]
