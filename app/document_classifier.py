from __future__ import annotations


def classify_document(text: str) -> tuple[str, float]:
    lowered = text.lower()
    scores = {
        "invoice": sum(term in lowered for term in ["invoice", "amount due", "payment terms", "bill to"]),
        "bank_statement_sample": sum(term in lowered for term in ["statement period", "opening balance", "closing balance", "transaction"]),
        "loan_agreement": sum(term in lowered for term in ["loan agreement", "borrower", "lender", "repayment", "principal"]),
        "financial_summary": sum(term in lowered for term in ["financial summary", "revenue", "expenses", "net income", "forecast"]),
    }
    document_type, score = max(scores.items(), key=lambda item: item[1])
    if score == 0:
        return "unknown", 0.35
    return document_type, min(0.95, 0.5 + (score * 0.12))
