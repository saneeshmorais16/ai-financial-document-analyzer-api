from __future__ import annotations

from app.extractors import extract_amounts, extract_dates, extract_entities, extract_structured_fields


def test_amount_extraction():
    amounts = extract_amounts("Amount Due: USD 12,500.00 and fee £250.00")
    assert {"raw": "USD 12,500.00", "value": 12500.0, "currency": "USD"} in amounts
    assert {"raw": "£250.00", "value": 250.0, "currency": "GBP"} in amounts


def test_date_extraction():
    dates = extract_dates("Invoice Date: 2026-03-14. Due: March 30, 2026.")
    assert "2026-03-14" in dates
    assert "March 30, 2026" in dates


def test_entity_extraction():
    entities = extract_entities("From: Demo Supplier LLC\nBill To: Sample Buyer Ltd")
    assert "Demo Supplier LLC" in entities
    assert "Sample Buyer Ltd" in entities


def test_structured_fields_confidence():
    fields = extract_structured_fields("From: A\nTo: B\nDate: 2026-01-01\nAmount: USD 100.00\nPayment Terms: Net 30\nBorrower shall pay.")
    assert fields["confidence"] >= 0.7
