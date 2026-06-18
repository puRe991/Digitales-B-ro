"""Starthelfer für CleverOffice Archiv.

Der Starter prüft die lokale Projektstruktur, legt bei Bedarf eine virtuelle
Umgebung an, installiert Abhängigkeiten und startet anschließend die Anwendung.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
APP_DIR = ROOT_DIR / "cleveroffice_archiv"
VENV_DIR = APP_DIR / ".venv"
REQUIREMENTS_FILE = APP_DIR / "requirements.txt"
MAIN_FILE = APP_DIR / "main.py"


def _venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def _run(command: list[str], *, cwd: Path) -> None:
    printable_command = " ".join(command)
    print(f"> {printable_command}")
    completed = subprocess.run(command, cwd=cwd, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"Befehl fehlgeschlagen ({completed.returncode}): {printable_command}")


def _validate_project() -> None:
    missing_paths = [path for path in (APP_DIR, REQUIREMENTS_FILE, MAIN_FILE) if not path.exists()]
    if missing_paths:
        formatted_paths = ", ".join(str(path.relative_to(ROOT_DIR)) for path in missing_paths)
        raise FileNotFoundError(f"Projektdateien fehlen: {formatted_paths}")


def _ensure_virtual_environment() -> Path:
    python_path = _venv_python()
    if python_path.exists():
        return python_path

    print("Virtuelle Umgebung wird erstellt ...")
    _run([sys.executable, "-m", "venv", str(VENV_DIR)], cwd=ROOT_DIR)
    if not python_path.exists():
        raise FileNotFoundError(f"Python der virtuellen Umgebung wurde nicht gefunden: {python_path}")
    return python_path


def _install_dependencies(python_path: Path) -> None:
    print("Abhängigkeiten werden installiert/aktualisiert ...")
    _run([str(python_path), "-m", "pip", "install", "--upgrade", "pip"], cwd=APP_DIR)
    _run([str(python_path), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)], cwd=APP_DIR)


def _start_application(python_path: Path) -> None:
    _run([str(python_path), str(MAIN_FILE)], cwd=APP_DIR)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Startet CleverOffice Archiv mit lokaler virtueller Umgebung.")
    parser.add_argument(
        "--skip-install",
        action="store_true",
        help="Installiert keine Abhängigkeiten und startet direkt mit der vorhandenen Umgebung.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        _validate_project()
        python_path = _ensure_virtual_environment()
        if not args.skip_install:
            _install_dependencies(python_path)
        _start_application(python_path)
    except (OSError, RuntimeError) as exc:
        print(f"Starter-Fehler: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
