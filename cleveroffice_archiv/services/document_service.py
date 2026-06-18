from datetime import datetime
from typing import Any, Optional
from database import get_connection

def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def optional_id(value: Any) -> Optional[int]:
    if value in (None, "", 0, "0"):
        return None
    return int(value)

from pathlib import Path
from file_manager import import_file


def create_document(title, source_path, document_date="", category="", case_id=None, status="offen", notes="") -> int:
    if not title.strip():
        raise ValueError("Bitte geben Sie einen Dokumenttitel ein.")
    stored = import_file(source_path)
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO documents(title, original_filename, stored_path, document_date, category, case_id, status, notes, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (title.strip(), Path(source_path).name, str(stored), document_date, category, optional_id(case_id), status, notes, now_iso()),
        )
        return int(cur.lastrowid)


def list_documents(search=""):
    with get_connection() as conn:
        if search.strip():
            like = f"%{search.strip()}%"
            return conn.execute(
                """SELECT d.*, c.title AS case_title FROM documents d LEFT JOIN cases c ON c.id=d.case_id
                   WHERE d.title LIKE ? OR d.original_filename LIKE ? OR d.category LIKE ? OR d.notes LIKE ?
                   ORDER BY d.created_at DESC""", (like, like, like, like)).fetchall()
        return conn.execute("""SELECT d.*, c.title AS case_title FROM documents d LEFT JOIN cases c ON c.id=d.case_id ORDER BY d.created_at DESC""").fetchall()


def recent_documents(limit=5):
    with get_connection() as conn:
        return conn.execute("SELECT * FROM documents ORDER BY created_at DESC LIMIT ?", (limit,)).fetchall()
