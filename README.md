# AI Financial Document Analyzer API

AI Financial Document Analyzer API is a portfolio-ready FastAPI project that analyses safe sample financial document text and extracts structured information, risk flags, summary points, and JSON output.

The first version works locally without any LLM API key. It uses rule-based NLP, regex extraction, and simple summarisation by default.

## Problem Statement

Financial documents often contain dates, parties, amounts, obligations, and risk language that need to be reviewed consistently. This starter project demonstrates how to turn unstructured sample text into structured output while keeping secrets and private financial data out of the repository.

## Why It Matters

The project shows practical backend engineering for AI/NLP-adjacent systems: document ingestion, extraction logic, risk flagging, confidence scoring, storage, API design, frontend presentation, automated tests, and safe project hygiene.

## Tech Stack

- Python
- FastAPI
- SQLite
- regex/entity extraction
- rule-based NLP
- Pydantic
- JavaScript, HTML, and CSS
- pytest
- GitHub Actions

## Core Features

- Paste document text.
- Upload text files.
- Classify safe sample document types: invoice, bank-style statement sample, loan agreement, and financial summary.
- Extract parties, dates, amounts, currencies, reference numbers, payment terms, and key obligations.
- Detect risk flags for missing dates, high amounts, late payment language, penalty clauses, unclear repayment terms, missing party names, and sensitive data warnings.
- Generate structured JSON output.
- Generate a short plain-English summary.
- Store analysis history in SQLite.

## Architecture Overview

```text
Frontend or API client
  -> FastAPI endpoint
  -> document classifier
  -> regex/entity extractors
  -> risk flag detector
  -> summary builder
  -> structured JSON response
  -> SQLite analysis history
```

## Example Input

```text
Invoice Number: INV-SAMPLE-1001
From: Northstar Demo Supplies
Bill To: River City Training Studio
Invoice Date: 2026-03-14
Amount Due: USD 4,250.00
Payment Terms: Net 30
The customer shall pay the full balance within 30 days.
```

## Example JSON Output

```json
{
  "id": 1,
  "source_name": "sample_invoice.txt",
  "document_type": "invoice",
  "summary": "Detected a invoice with Northstar Demo Supplies, River City Training Studio. Extracted 1 amount(s), 1 date(s), and 0 risk flag(s). Review flagged items manually before relying on the result.",
  "confidence": 0.83,
  "extracted_fields": {
    "parties": ["Northstar Demo Supplies", "River City Training Studio"],
    "dates": ["2026-03-14"],
    "amounts": [{"raw": "USD 4,250.00", "value": 4250.0, "currency": "USD"}],
    "currencies": ["USD"],
    "references": ["INV-SAMPLE-1001"],
    "payment_terms": ["Payment Terms: Net 30"],
    "key_obligations": ["The customer shall pay the full balance within 30 days"],
    "confidence": 0.95
  },
  "risk_flags": []
}
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

## Run the API

```bash
python run.py
```

Or:

```bash
uvicorn app.main:app --reload
```

Open the frontend:

```text
http://127.0.0.1:8000
```

Use a different local port with `PORT=8001 python run.py` if another demo is already running.

Health check:

```text
GET http://127.0.0.1:8000/health
```

Analyze text:

```bash
curl -X POST "http://127.0.0.1:8000/analyze/text" \
  -H "Content-Type: application/json" \
  -d '{"source_name":"sample_invoice.txt","text":"Invoice Date: 2026-03-14\nFrom: Demo Vendor\nBill To: Demo Buyer\nAmount Due: USD 100.00\nPayment Terms: Net 30"}'
```

## Run Tests

```bash
pytest
```

GitHub Actions runs the same test command on pushes and pull requests.

## Responsible AI and Limitations

- This starter project uses deterministic rules and regex extraction, not regulated financial analysis.
- Results can contain false positives, false negatives, and incomplete extraction.
- Optional LLM fields are placeholders only and no external LLM call is required.
- Do not process private financial documents without appropriate privacy, security, retention, and consent controls.
- This project does not claim production readiness, real clients, or regulated financial compliance.

## Financial and Legal Disclaimer

This project is for educational and portfolio demonstration purposes only. It does not provide financial, legal, accounting, lending, compliance, tax, or investment advice. Extracted fields and risk flags must be reviewed by qualified humans before any decision is made.

## Future Improvements

- Add PDF and DOCX parsing with redaction safeguards.
- Add local NLP model support for richer entity extraction.
- Add configurable risk thresholds and rule sets.
- Add optional LLM summaries after privacy controls are implemented.
- Add SARIF or audit-style exports.
- Add authentication and per-user analysis history for hosted deployments.

## No-Secrets Note

Do not commit API keys, `.env` files, tokens, credentials, passwords, private financial documents, personal data, logs, generated PDFs, temporary application packets, SQLite databases, uploads, or generated outputs. Use only fake sample documents in the repository.
