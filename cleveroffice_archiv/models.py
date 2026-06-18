from dataclasses import dataclass
from typing import Optional


@dataclass
class Case:
    id: Optional[int]
    title: str
    description: str = ""
    case_type: str = "Privat"
    status: str = "aktiv"
    created_at: str = ""


@dataclass
class Document:
    id: Optional[int]
    title: str
    original_filename: str
    stored_path: str
    document_date: str = ""
    category: str = ""
    case_id: Optional[int] = None
    status: str = "offen"
    notes: str = ""
    created_at: str = ""


@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str = ""
    due_date: str = ""
    status: str = "offen"
    case_id: Optional[int] = None
    document_id: Optional[int] = None
    created_at: str = ""


@dataclass
class Deadline:
    id: Optional[int]
    title: str
    due_date: str
    reminder_date: str = ""
    status: str = "offen"
    case_id: Optional[int] = None
    document_id: Optional[int] = None
    created_at: str = ""


@dataclass
class Contact:
    id: Optional[int]
    name: str
    organization: str = ""
    role: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    notes: str = ""
    created_at: str = ""
