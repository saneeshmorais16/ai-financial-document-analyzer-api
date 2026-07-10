# Project Status

## Current Build Status

Starter implementation is complete locally. GitHub Actions is configured to run tests on pushes and pull requests.

## Completed Features

- Paste-text financial document analysis.
- Text file upload analysis.
- Safe sample document support for invoices, bank-style statements, loan agreements, and financial summaries.
- Rule-based document classification.
- Regex/entity extraction for parties, dates, amounts, currencies, references, payment terms, and key obligations.
- Risk flags for missing dates, high amounts, late payment language, penalty clauses, unclear repayment terms, missing parties, and sensitive data warnings.
- Plain-English summary generation.
- Confidence scoring for extracted fields.
- SQLite analysis history.
- Simple frontend for paste/upload analysis, extracted JSON, risk flags, and summary.
- Tests for extraction, risk flags, service output, health endpoint, and analysis endpoint.

## Remaining Improvements

- Add real document parsing for PDFs and DOCX files after a safe redaction workflow is designed.
- Add richer named entity recognition with a local NLP model.
- Add configurable thresholds and risk rules.
- Add optional LLM provider adapters with privacy controls.
- Add authentication, rate limits, and file size limits for hosted use.

## Testing Status

Latest local check:

- `pytest`: 9 passed

Run locally with:

```bash
pytest
```

## What Must Be Checked Before Making Public

- Confirm no `.env` files, credentials, logs, databases, uploads, private documents, local data, or generated outputs are tracked.
- Confirm examples are fake samples only.
- Confirm README does not claim production use, real clients, or regulated compliance.
- Confirm optional LLM fields remain placeholders only.

## Files That Must Never Be Committed

- `.env`
- `.env.*`
- API keys, tokens, credentials, passwords, or private configuration
- `*.db`, `*.sqlite`, `*.sqlite3`
- Private financial documents
- Real bank statements, payslips, IDs, invoices, contracts, or personal financial data
- Logs and generated PDFs
- `application_packets/`
- `generated_outputs/`
- `secrets/`
- `credentials/`
- `uploads/`
- `private_documents/`
- `local_data/`
