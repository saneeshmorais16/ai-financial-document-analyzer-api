from __future__ import annotations

from app.analysis_service import analyze_text


def test_analysis_service_returns_structured_output():
    result = analyze_text(
        "Invoice Number: INV-SAMPLE-1\nFrom: Demo Vendor\nBill To: Demo Buyer\nInvoice Date: 2026-02-01\nAmount Due: USD 500.00\nPayment Terms: Net 15",
        "sample_invoice.txt",
    )
    assert result["document_type"] == "invoice"
    assert result["confidence"] > 0.5
    assert result["extracted_fields"]["amounts"][0]["currency"] == "USD"
    assert "summary" in result
