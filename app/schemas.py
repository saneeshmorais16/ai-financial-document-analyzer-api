from __future__ import annotations

from pydantic import BaseModel, Field


class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1)
    source_name: str = "pasted_text"


class Amount(BaseModel):
    raw: str
    value: float
    currency: str


class ExtractedFields(BaseModel):
    parties: list[str]
    dates: list[str]
    amounts: list[Amount]
    currencies: list[str]
    references: list[str]
    payment_terms: list[str]
    key_obligations: list[str]
    confidence: float


class RiskFlag(BaseModel):
    flag_type: str
    severity: str
    explanation: str
    suggested_review: str


class AnalysisResponse(BaseModel):
    id: int | None = None
    source_name: str
    document_type: str
    summary: str
    confidence: float
    extracted_fields: ExtractedFields
    risk_flags: list[RiskFlag]
