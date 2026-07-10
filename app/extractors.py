from __future__ import annotations

import re
from dataclasses import dataclass


DATE_PATTERN = re.compile(
    r"\b(?:\d{4}-\d{2}-\d{2}|\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{4})\b",
    re.IGNORECASE,
)
AMOUNT_PATTERN = re.compile(r"(?P<currency>USD|GBP|EUR|\$|£|€)\s?(?P<amount>\d{1,3}(?:,\d{3})*(?:\.\d{2})?|\d+(?:\.\d{2})?)", re.IGNORECASE)
REFERENCE_PATTERN = re.compile(r"\b(?:invoice|account|reference|loan|statement)\s*(?:number|no\.?|id|ref)?\s*[:#-]\s*([A-Z0-9-]{4,})", re.IGNORECASE)
ENTITY_LINE_PATTERN = re.compile(r"^\s*(?:from|to|bill to|vendor|customer|borrower|lender|prepared for|issuer)\s*:\s*(.+)$", re.IGNORECASE | re.MULTILINE)
PAYMENT_TERMS_PATTERN = re.compile(r"\b(?:net\s+\d+|due\s+(?:on receipt|within\s+\d+\s+days)|payment terms\s*:\s*.+|repay(?:ment)?\s+terms\s*:\s*.+)\b", re.IGNORECASE)
OBLIGATION_PATTERN = re.compile(r"\b(?:must|shall|agrees to|is required to|will pay|repay|deliver|provide)\b.+", re.IGNORECASE)

CURRENCY_MAP = {"$": "USD", "£": "GBP", "€": "EUR"}


@dataclass
class ExtractedAmount:
    raw: str
    value: float
    currency: str


def extract_dates(text: str) -> list[str]:
    return sorted(set(match.group(0) for match in DATE_PATTERN.finditer(text)))


def extract_amounts(text: str) -> list[dict]:
    amounts = []
    seen = set()
    for match in AMOUNT_PATTERN.finditer(text):
        raw = match.group(0)
        value = float(match.group("amount").replace(",", ""))
        currency = CURRENCY_MAP.get(match.group("currency"), match.group("currency").upper())
        key = (raw, value, currency)
        if key in seen:
            continue
        seen.add(key)
        amounts.append({"raw": raw, "value": value, "currency": currency})
    return amounts


def extract_entities(text: str) -> list[str]:
    entities = []
    for match in ENTITY_LINE_PATTERN.finditer(text):
        entity = match.group(1).strip().rstrip(".")
        if entity and entity not in entities:
            entities.append(entity)
    return entities


def extract_references(text: str) -> list[str]:
    return sorted(set(match.group(1) for match in REFERENCE_PATTERN.finditer(text)))


def extract_payment_terms(text: str) -> list[str]:
    terms = []
    for match in PAYMENT_TERMS_PATTERN.finditer(text):
        term = match.group(0).strip()
        if term not in terms:
            terms.append(term)
    return terms


def extract_key_obligations(text: str) -> list[str]:
    obligations = []
    for line in text.splitlines():
        cleaned = line.strip().rstrip(".")
        if OBLIGATION_PATTERN.search(cleaned):
            obligations.append(cleaned)
    return obligations[:8]


def extraction_confidence(extracted: dict) -> float:
    weighted_checks = [
        bool(extracted.get("dates")),
        bool(extracted.get("amounts")),
        bool(extracted.get("parties")),
        bool(extracted.get("payment_terms")),
        bool(extracted.get("key_obligations")),
    ]
    return round(0.35 + (sum(weighted_checks) / len(weighted_checks)) * 0.6, 2)


def extract_structured_fields(text: str) -> dict:
    fields = {
        "parties": extract_entities(text),
        "dates": extract_dates(text),
        "amounts": extract_amounts(text),
        "currencies": sorted({amount["currency"] for amount in extract_amounts(text)}),
        "references": extract_references(text),
        "payment_terms": extract_payment_terms(text),
        "key_obligations": extract_key_obligations(text),
    }
    fields["confidence"] = extraction_confidence(fields)
    return fields
