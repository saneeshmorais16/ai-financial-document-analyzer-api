from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analysis_endpoint(tmp_path, monkeypatch):
    db_url = f"sqlite:///{tmp_path / 'analyses.db'}"
    monkeypatch.setattr("app.storage.get_connection", lambda: __import__("app.database").database.get_connection(db_url))
    monkeypatch.setattr("app.storage.init_db", lambda: __import__("app.database").database.init_db(db_url))

    client = TestClient(app)
    response = client.post(
        "/analyze/text",
        json={
            "source_name": "fake_invoice.txt",
            "text": "Invoice Number: INV-FAKE-1\nFrom: Demo Vendor\nBill To: Demo Buyer\nInvoice Date: 2026-01-15\nAmount Due: USD 1,200.00\nPayment Terms: Net 30",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["id"] >= 1
    assert body["document_type"] == "invoice"
    assert body["extracted_fields"]["amounts"][0]["value"] == 1200.0
