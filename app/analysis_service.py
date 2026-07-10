from __future__ import annotations

from app.document_classifier import classify_document
from app.extractors import extract_structured_fields
from app.risk_flags import detect_risk_flags
from app.summarizer import build_summary


def analyze_text(text: str, source_name: str = "pasted_text") -> dict:
    document_type, type_confidence = classify_document(text)
    fields = extract_structured_fields(text)
    risk_flags = detect_risk_flags(text, fields)
    summary = build_summary(document_type, fields, risk_flags)
    overall_confidence = round((type_confidence + fields["confidence"]) / 2, 2)

    return {
        "id": None,
        "source_name": source_name,
        "document_type": document_type,
        "summary": summary,
        "confidence": overall_confidence,
        "extracted_fields": fields,
        "risk_flags": risk_flags,
    }
