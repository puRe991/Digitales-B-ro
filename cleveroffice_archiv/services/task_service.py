from database import get_connection
from services.shared import now_iso, optional_id, validate_limit

def create_task(title, description="", due_date="", status="offen", case_id=None, document_id=None) -> int:
    if not title.strip():
        raise ValueError("Bitte geben Sie einen Aufgabentitel ein.")
    with get_connection() as conn:
        cur = conn.execute("INSERT INTO tasks(title, description, due_date, status, case_id, document_id, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                           (title.strip(), description, due_date, status, optional_id(case_id), optional_id(document_id), now_iso()))
        return int(cur.lastrowid)

def list_tasks(open_only=False, limit=None):
    sql = "SELECT t.*, c.title AS case_title, d.title AS document_title FROM tasks t LEFT JOIN cases c ON c.id=t.case_id LEFT JOIN documents d ON d.id=t.document_id"
    params = []
    if open_only:
        sql += " WHERE t.status != 'erledigt'"
    sql += " ORDER BY COALESCE(t.due_date, '9999-12-31') ASC, t.created_at DESC"
    if limit is not None:
        sql += " LIMIT ?"
        params.append(validate_limit(limit))
    with get_connection() as conn:
        return conn.execute(sql, params).fetchall()
