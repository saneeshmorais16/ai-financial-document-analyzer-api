from __future__ import annotations

from app.extractors import extract_structured_fields
from app.risk_flags import detect_risk_flags


def test_risk_flag_detection():
    text = "Borrower: Example Co\nAmount: USD 250,000.00\nPayment is past due and a penalty applies."
    fields = extract_structured_fields(text)
    flags = detect_risk_flags(text, fields)
    flag_types = {flag["flag_type"] for flag in flags}
    assert "unusually_high_amount" in flag_types
    assert "late_payment_language" in flag_types
    assert "penalty_clause" in flag_types


def test_missing_date_flag():
    fields = extract_structured_fields("From: Demo Co\nAmount: USD 100.00")
    flags = detect_risk_flags("From: Demo Co\nAmount: USD 100.00", fields)
    assert any(flag["flag_type"] == "missing_dates" for flag in flags)
