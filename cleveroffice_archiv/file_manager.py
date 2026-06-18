import os
import re
import shutil
from pathlib import Path
from database import DOCUMENTS_DIR

_SAFE_CHARS = re.compile(r"[^A-Za-z0-9._ -]+")


def safe_filename(filename: str) -> str:
    name = Path(filename).name.strip() or "dokument"
    sanitized = _SAFE_CHARS.sub("_", name).strip(" .")
    return sanitized or "dokument"


def unique_destination(filename: str) -> Path:
    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    safe = safe_filename(filename)
    candidate = DOCUMENTS_DIR / safe
    if not candidate.exists():
        return candidate
    stem, suffix = candidate.stem, candidate.suffix
    counter = 1
    while True:
        next_candidate = DOCUMENTS_DIR / f"{stem}_{counter}{suffix}"
        if not next_candidate.exists():
            return next_candidate
        counter += 1


def import_file(source_path: str) -> Path:
    source = Path(source_path)
    if not source.is_file():
        raise FileNotFoundError(f"Die Datei wurde nicht gefunden: {source_path}")
    destination = unique_destination(source.name)
    shutil.copy2(source, destination)
    return destination


def open_file(path: str) -> None:
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Die gespeicherte Datei existiert nicht mehr: {path}")
    os.startfile(str(file_path))  # type: ignore[attr-defined]  # Windows-Zielplattform
