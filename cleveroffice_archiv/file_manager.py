from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
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
    source = Path(source_path).expanduser()
    if not source_path or not source.is_file():
        raise FileNotFoundError(f"Die Datei wurde nicht gefunden: {source_path}")

    source = source.resolve()
    destination = unique_destination(source.name)
    if source == destination.resolve():
        raise ValueError("Die Quelldatei liegt bereits im Dokumentenarchiv.")

    shutil.copy2(source, destination)
    return destination


def remove_imported_file(path: Path) -> None:
    """Best-effort cleanup for files copied before a failed database write."""
    try:
        resolved = path.resolve()
        documents_root = DOCUMENTS_DIR.resolve()
        if resolved.is_file() and resolved.parent == documents_root:
            resolved.unlink()
    except OSError:
        # Cleanup must not hide the original database/import error.
        return


def open_file(path: str) -> None:
    file_path = Path(path).expanduser()
    if not file_path.exists():
        raise FileNotFoundError(f"Die gespeicherte Datei existiert nicht mehr: {path}")

    if os.name == "nt":
        os.startfile(str(file_path))  # type: ignore[attr-defined]
        return
    if sys.platform == "darwin":
        subprocess.Popen(["open", str(file_path)])
        return
    subprocess.Popen(["xdg-open", str(file_path)])
