from __future__ import annotations


def build_summary(document_type: str, fields: dict, risk_flags: list[dict]) -> str:
    parties = ", ".join(fields.get("parties", [])[:3]) or "no clear parties"
    amount_count = len(fields.get("amounts", []))
    date_count = len(fields.get("dates", []))
    risk_count = len(risk_flags)
    return (
        f"Detected a {document_type.replace('_', ' ')} with {parties}. "
        f"Extracted {amount_count} amount(s), {date_count} date(s), and {risk_count} risk flag(s). "
        "Review flagged items manually before relying on the result."
    )
