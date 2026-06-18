from datetime import datetime
from typing import Any, Optional
from database import get_connection

def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def optional_id(value: Any) -> Optional[int]:
    if value in (None, "", 0, "0"):
        return None
    return int(value)

def create_case(title, description="", case_type="Privat", status="aktiv") -> int:
    if not title.strip():
        raise ValueError("Bitte geben Sie einen Aktentitel ein.")
    with get_connection() as conn:
        cur = conn.execute("INSERT INTO cases(title, description, case_type, status, created_at) VALUES (?, ?, ?, ?, ?)",
                           (title.strip(), description, case_type, status, now_iso()))
        return int(cur.lastrowid)

def list_cases():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM cases ORDER BY created_at DESC").fetchall()

def case_options():
    return [(None, "Keine Akte")] + [(r["id"], r["title"]) for r in list_cases()]
