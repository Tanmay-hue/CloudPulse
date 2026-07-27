from fastapi.testclient import TestClient
from app.main import app


def test_home():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200


def test_ready():
    with TestClient(app) as client:
        response = client.get("/ready")
        assert response.status_code == 200


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200


def test_version():
    with TestClient(app) as client:
        response = client.get("/version")
        assert response.status_code == 200