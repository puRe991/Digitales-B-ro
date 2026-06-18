"""Qt-Kompatibilitätsschicht für CleverOffice Archiv.

PySide6 liefert keine 32-Bit-Windows-Wheels. PyQt5 bietet weiterhin passende
win32-Wheels und reicht für die in dieser Anwendung genutzten Widgets aus.
Alle UI-Module importieren Qt-Klassen über dieses Modul, damit die konkrete
Qt-Bindung an einer Stelle austauschbar bleibt.
"""

from __future__ import annotations

try:
    from PyQt5.QtCore import QDate
    from PyQt5.QtWidgets import (
        QApplication,
        QComboBox,
        QDateEdit,
        QDialog,
        QFileDialog,
        QFormLayout,
        QHBoxLayout,
        QHeaderView,
        QLabel,
        QLineEdit,
        QListWidget,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QStackedWidget,
        QTableWidget,
        QTableWidgetItem,
        QTextEdit,
        QVBoxLayout,
        QWidget,
    )
except ImportError as exc:  # pragma: no cover - depends on local installation
    raise ImportError(
        "Qt konnte nicht geladen werden. Installieren Sie die Abhängigkeiten mit "
        "`python start_cleveroffice.py` oder `python -m pip install -r "
        "cleveroffice_archiv/requirements.txt`. Falls die Abhängigkeiten bereits "
        "installiert sind, fehlen wahrscheinlich Betriebssystem-Bibliotheken für Qt."
    ) from exc

__all__ = [
    "QApplication",
    "QComboBox",
    "QDate",
    "QDateEdit",
    "QDialog",
    "QFileDialog",
    "QFormLayout",
    "QHBoxLayout",
    "QHeaderView",
    "QLabel",
    "QLineEdit",
    "QListWidget",
    "QMainWindow",
    "QMessageBox",
    "QPushButton",
    "QStackedWidget",
    "QTableWidget",
    "QTableWidgetItem",
    "QTextEdit",
    "QVBoxLayout",
    "QWidget",
]
