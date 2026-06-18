from database import get_connection
from services.shared import now_iso


def create_contact(name, organization="", role="", phone="", email="", address="", notes="") -> int:
    if not name.strip():
        raise ValueError("Bitte geben Sie einen Namen ein.")
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO contacts(name, organization, role, phone, email, address, notes, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (name.strip(), organization, role, phone, email, address, notes, now_iso()),
        )
        return int(cur.lastrowid)


def list_contacts():
    with get_connection() as conn:
        return conn.execute("SELECT * FROM contacts ORDER BY name ASC").fetchall()
