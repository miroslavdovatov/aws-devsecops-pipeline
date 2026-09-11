from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 500 #intentional mistake to test the gate function
    assert response.json() == {"status": "healthy"}

def test_api_data():
    response = client.get("/api/data")
    assert response.status_code == 200
    assert response.json()["status"] == "success"