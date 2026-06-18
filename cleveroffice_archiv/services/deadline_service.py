from datetime import datetime
from typing import Any, Optional
from database import get_connection

def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def optional_id(value: Any) -> Optional[int]:
    if value in (None, "", 0, "0"):
        return None
    return int(value)

def create_deadline(title, due_date, reminder_date="", status="offen", case_id=None, document_id=None) -> int:
    if not title.strip():
        raise ValueError("Bitte geben Sie einen Fristtitel ein.")
    if not due_date:
        raise ValueError("Bitte geben Sie ein Fälligkeitsdatum ein.")
    with get_connection() as conn:
        cur = conn.execute("INSERT INTO deadlines(title, due_date, reminder_date, status, case_id, document_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (title.strip(), due_date, reminder_date, status, optional_id(case_id), optional_id(document_id), now_iso()))
        return int(cur.lastrowid)

def list_deadlines(open_only=False, limit=None):
    sql = "SELECT dl.*, c.title AS case_title, d.title AS document_title FROM deadlines dl LEFT JOIN cases c ON c.id=dl.case_id LEFT JOIN documents d ON d.id=dl.document_id"
    params = []
    if open_only:
        sql += " WHERE dl.status = 'offen'"
    sql += " ORDER BY dl.due_date ASC"
    if limit:
        sql += " LIMIT ?"; params.append(limit)
    with get_connection() as conn:
        return conn.execute(sql, params).fetchall()
