from fastapi.testclient import TestClient
from app.main import app 


client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model_loaded"] is True
    assert "model_version" in body


def test_predict_returns_valid_score():
    response = client.post("/predict", json={"features":[0.5, -1.2, 3.0]})
    assert response.status_code == 200
    body = response.json()
    assert 0.0 <= body["fraud_probability"] <= 1.0
    assert body["model_version"] == "0.0.1-stub"

def test_predict_rejects_bad_input():
    response = client.post("/predict", json={"features": "not a list"})
    assert response.status_code == 422
