import json
from app.app import app

def test_healthz():
    client = app.test_client()
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "ok"

def test_predict_missing_text():
    client = app.test_client()
    resp = client.post("/predict", json={})
    assert resp.status_code == 400

def test_metrics():
    client = app.test_client()
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"app_requests_total" in resp.data
