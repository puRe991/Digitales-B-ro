import sqlite3
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
DB_PATH = DATA_DIR / "cleveroffice.db"
DOCUMENTS_DIR = DATA_DIR / "documents"


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                case_type TEXT,
                status TEXT DEFAULT 'aktiv',
                created_at TEXT
            );

            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                original_filename TEXT,
                stored_path TEXT NOT NULL,
                document_date TEXT,
                category TEXT,
                case_id INTEGER,
                status TEXT DEFAULT 'offen',
                notes TEXT,
                created_at TEXT,
                FOREIGN KEY(case_id) REFERENCES cases(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                status TEXT DEFAULT 'offen',
                case_id INTEGER,
                document_id INTEGER,
                created_at TEXT,
                FOREIGN KEY(case_id) REFERENCES cases(id) ON DELETE SET NULL,
                FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS deadlines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due_date TEXT NOT NULL,
                reminder_date TEXT,
                status TEXT DEFAULT 'offen',
                case_id INTEGER,
                document_id INTEGER,
                created_at TEXT,
                FOREIGN KEY(case_id) REFERENCES cases(id) ON DELETE SET NULL,
                FOREIGN KEY(document_id) REFERENCES documents(id) ON DELETE SET NULL
            );

            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                organization TEXT,
                role TEXT,
                phone TEXT,
                email TEXT,
                address TEXT,
                notes TEXT,
                created_at TEXT
            );

            CREATE INDEX IF NOT EXISTS idx_documents_search ON documents(title, original_filename, category);
            CREATE INDEX IF NOT EXISTS idx_tasks_status_due ON tasks(status, due_date);
            CREATE INDEX IF NOT EXISTS idx_deadlines_status_due ON deadlines(status, due_date);
            """
        )
