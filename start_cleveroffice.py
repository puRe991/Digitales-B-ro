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

MIN_QT_PYTHON = (3, 8)


class StarterError(RuntimeError):
    """Fehler mit nutzerfreundlicher Ausgabe für den Starter."""


def _venv_python() -> Path:
    if os.name == "nt":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def _run(command: list[str], *, cwd: Path) -> None:
    printable_command = " ".join(command)
    print(f"> {printable_command}")
    completed = subprocess.run(command, cwd=cwd, check=False)
    if completed.returncode != 0:
        raise StarterError(f"Befehl fehlgeschlagen ({completed.returncode}): {printable_command}")


def _run_with_context(command: list[str], *, cwd: Path, context: str) -> None:
    try:
        _run(command, cwd=cwd)
    except StarterError as exc:
        raise StarterError(f"{exc}\n\n{context}") from exc


def _validate_project() -> None:
    missing_paths = [path for path in (APP_DIR, REQUIREMENTS_FILE, MAIN_FILE) if not path.exists()]
    if missing_paths:
        formatted_paths = ", ".join(str(path.relative_to(ROOT_DIR)) for path in missing_paths)
        raise FileNotFoundError(f"Projektdateien fehlen: {formatted_paths}")


def _ensure_virtual_environment() -> Path:
    python_path = _venv_python()
    if python_path.exists():
        return python_path

    _validate_python_runtime(sys.version_info, executable=Path(sys.executable))
    print("Virtuelle Umgebung wird erstellt ...")
    _run([sys.executable, "-m", "venv", str(VENV_DIR)], cwd=ROOT_DIR)
    if not python_path.exists():
        raise FileNotFoundError(f"Python der virtuellen Umgebung wurde nicht gefunden: {python_path}")
    return python_path


def _python_runtime(python_path: Path) -> tuple[tuple[int, int, int], str]:
    command = [
        str(python_path),
        "-c",
        "import sys; "
        "print(f'{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}'); "
        "print(sys.executable)",
    ]
    completed = subprocess.run(command, cwd=APP_DIR, check=False, capture_output=True, text=True)
    if completed.returncode != 0:
        details = completed.stderr.strip() or completed.stdout.strip() or "keine Details"
        raise StarterError(f"Python der virtuellen Umgebung konnte nicht geprüft werden: {details}")

    lines = completed.stdout.splitlines()
    if len(lines) < 2:
        raise StarterError("Python der virtuellen Umgebung lieferte unvollständige Versionsinformationen.")

    version = tuple(int(part) for part in lines[0].split(".", maxsplit=2))
    return version, lines[1].strip()


def _validate_python_runtime(version_info: tuple[int, ...], *, executable: Path) -> None:
    major_minor = version_info[:2]
    if major_minor < MIN_QT_PYTHON:
        raise StarterError(
            "Die Qt-Oberfläche kann mit dieser Python-Version nicht installiert werden.\n"
            f"Gefunden: Python {'.'.join(map(str, version_info[:3]))} ({executable})\n"
            "Benötigt: CPython ab 3.8. Installieren Sie eine aktuellere Python-Version "
            "und erstellen Sie die virtuelle Umgebung neu."
        )


def _validate_venv_runtime(python_path: Path) -> None:
    version, executable = _python_runtime(python_path)
    _validate_python_runtime(version, executable=Path(executable))


def _qt_install_hint() -> str:
    return (
        "Hinweis zur Qt-Installation:\n"
        "- Dieses Projekt nutzt PyQt5, weil PySide6 keine 32-Bit-Windows-Umgebungen unterstützt.\n"
        "- Wenn Sie Python aktualisiert haben, löschen Sie `cleveroffice_archiv\\.venv` und starten Sie erneut.\n"
        "- Firmen-Proxys oder private Paketquellen können PyQt5-Wheels blockieren; testen Sie dann "
        "`python -m pip index versions PyQt5`."
    )


def _install_dependencies(python_path: Path) -> None:
    _validate_venv_runtime(python_path)
    print("Abhängigkeiten werden installiert/aktualisiert ...")
    _run([str(python_path), "-m", "pip", "install", "--upgrade", "pip"], cwd=APP_DIR)
    _run_with_context(
        [str(python_path), "-m", "pip", "install", "-r", str(REQUIREMENTS_FILE)],
        cwd=APP_DIR,
        context=_qt_install_hint(),
    )


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
    except (OSError, StarterError) as exc:
        print(f"Starter-Fehler: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
