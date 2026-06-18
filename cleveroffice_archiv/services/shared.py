from __future__ import annotations

from datetime import datetime
from typing import Any, Optional


def now_iso() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def optional_id(value: Any) -> Optional[int]:
    if value in (None, "", 0, "0"):
        return None
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Ungültige ID: {value!r}") from exc


def validate_limit(value: Any, *, default: int = 100, maximum: int = 1000) -> int:
    if value in (None, ""):
        return default
    try:
        limit = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Ungültiges Limit: {value!r}") from exc
    if limit < 1:
        raise ValueError("Limit muss größer als 0 sein.")
    return min(limit, maximum)
