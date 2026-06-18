from __future__ import annotations

from pathlib import Path

from database import get_connection
from file_manager import import_file, remove_imported_file
from services.shared import now_iso, optional_id, validate_limit


def create_document(title, source_path, document_date="", category="", case_id=None, status="offen", notes="") -> int:
    cleaned_title = title.strip()
    if not cleaned_title:
        raise ValueError("Bitte geben Sie einen Dokumenttitel ein.")

    stored = import_file(source_path)
    try:
        with get_connection() as conn:
            cur = conn.execute(
                """INSERT INTO documents(title, original_filename, stored_path, document_date, category, case_id, status, notes, created_at)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    cleaned_title,
                    Path(source_path).name,
                    str(stored),
                    document_date,
                    category,
                    optional_id(case_id),
                    status,
                    notes,
                    now_iso(),
                ),
            )
            return int(cur.lastrowid)
    except Exception:
        remove_imported_file(stored)
        raise


def list_documents(search=""):
    with get_connection() as conn:
        if search.strip():
            like = f"%{search.strip()}%"
            return conn.execute(
                """SELECT d.*, c.title AS case_title FROM documents d LEFT JOIN cases c ON c.id=d.case_id
                   WHERE d.title LIKE ? OR d.original_filename LIKE ? OR d.category LIKE ? OR d.notes LIKE ?
                   ORDER BY d.created_at DESC""",
                (like, like, like, like),
            ).fetchall()
        return conn.execute(
            """SELECT d.*, c.title AS case_title FROM documents d LEFT JOIN cases c ON c.id=d.case_id ORDER BY d.created_at DESC"""
        ).fetchall()


def recent_documents(limit=5):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM documents ORDER BY created_at DESC LIMIT ?", (validate_limit(limit),)).fetchall()
