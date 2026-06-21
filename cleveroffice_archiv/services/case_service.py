from database import get_connection
from services.shared import now_iso


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


def get_case(case_id):
    """Return one case by id or None when it no longer exists."""
    if case_id is None:
        return None
    with get_connection() as conn:
        return conn.execute("SELECT * FROM cases WHERE id = ?", (case_id,)).fetchone()


def case_options():
    return [(None, "Keine Akte")] + [(r["id"], r["title"]) for r in list_cases()]


def case_overview(case_id):
    """Load all information needed for the case preview pane."""
    case = get_case(case_id)
    if case is None:
        return None

    with get_connection() as conn:
        documents = conn.execute(
            """SELECT d.*, c.title AS case_title
               FROM documents d
               LEFT JOIN cases c ON c.id = d.case_id
               WHERE d.case_id = ?
               ORDER BY d.created_at DESC""",
            (case_id,),
        ).fetchall()
        tasks = conn.execute(
            """SELECT t.*, d.title AS document_title
               FROM tasks t
               LEFT JOIN documents d ON d.id = t.document_id
               WHERE t.case_id = ?
               ORDER BY COALESCE(t.due_date, '9999-12-31') ASC, t.created_at DESC""",
            (case_id,),
        ).fetchall()
        deadlines = conn.execute(
            """SELECT dl.*, d.title AS document_title
               FROM deadlines dl
               LEFT JOIN documents d ON d.id = dl.document_id
               WHERE dl.case_id = ?
               ORDER BY dl.due_date ASC""",
            (case_id,),
        ).fetchall()

    return {
        "case": case,
        "documents": documents,
        "tasks": tasks,
        "deadlines": deadlines,
    }
