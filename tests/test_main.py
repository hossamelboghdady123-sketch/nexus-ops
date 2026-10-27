from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Ship with confidence." in response.text
    assert "NEXUS Ops" in response.text


def test_api_info():
    response = client.get("/api")
    assert response.status_code == 200
    assert response.json()["service"] == "NEXUS Ops"
    assert response.json()["status"] == "running"


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "timestamp" in response.json()


def test_api_documentation():
    response = client.get("/docs")
    assert response.status_code == 200
