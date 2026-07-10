from __future__ import annotations

import json
from datetime import datetime, timezone

from fastapi import HTTPException

from app.database import get_connection, init_db


def save_analysis(analysis: dict) -> int:
    init_db()
    with get_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO analyses (created_at, document_type, summary, payload) VALUES (?, ?, ?, ?)",
            (
                datetime.now(timezone.utc).isoformat(),
                analysis["document_type"],
                analysis["summary"],
                json.dumps(analysis),
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)


def list_analyses() -> list[dict]:
    init_db()
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, created_at, document_type, summary FROM analyses ORDER BY id DESC LIMIT 50"
        ).fetchall()
    return [dict(row) for row in rows]


def get_analysis(analysis_id: int) -> dict:
    init_db()
    with get_connection() as connection:
        row = connection.execute("SELECT payload FROM analyses WHERE id = ?", (analysis_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    payload = json.loads(row["payload"])
    payload["id"] = analysis_id
    return payload
