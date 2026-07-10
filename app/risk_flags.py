from __future__ import annotations

import re

from app.config import HIGH_AMOUNT_THRESHOLD


def _flag(flag_type: str, severity: str, explanation: str, suggested_review: str) -> dict:
    return {
        "flag_type": flag_type,
        "severity": severity,
        "explanation": explanation,
        "suggested_review": suggested_review,
    }


def detect_risk_flags(text: str, fields: dict) -> list[dict]:
    lowered = text.lower()
    flags = []

    if not fields.get("dates"):
        flags.append(_flag("missing_dates", "medium", "No clear date was extracted.", "Confirm issue, due, statement, or signing dates."))

    if not fields.get("parties"):
        flags.append(_flag("missing_party_name", "medium", "No named party/entity was extracted.", "Check that payer/payee, borrower/lender, or issuer names are present."))

    if any(amount["value"] >= HIGH_AMOUNT_THRESHOLD for amount in fields.get("amounts", [])):
        flags.append(_flag("unusually_high_amount", "high", "At least one extracted amount is above the configured review threshold.", "Manually verify the amount, currency, and approval context."))

    if re.search(r"\b(overdue|past due|late payment|delinquent)\b", lowered):
        flags.append(_flag("late_payment_language", "high", "Late or overdue payment language is present.", "Review timing, penalties, and remediation steps."))

    if re.search(r"\b(penalty|default interest|late fee|liquidated damages)\b", lowered):
        flags.append(_flag("penalty_clause", "high", "Penalty or default language is present.", "Have a qualified reviewer inspect the clause and obligations."))

    if re.search(r"\b(to be agreed|tbd|at lender discretion|subject to change)\b", lowered):
        flags.append(_flag("unclear_repayment_terms", "medium", "Repayment or payment terms appear unclear.", "Clarify repayment dates, amounts, and decision rights."))

    if re.search(r"\b(ssn|social security|passport|tax id|card number)\b", lowered):
        flags.append(_flag("sensitive_data_warning", "critical", "Sensitive personal or financial identifier language is present.", "Remove or redact sensitive data before sharing or storing."))

    return flags
