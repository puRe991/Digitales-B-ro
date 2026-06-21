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
        QGroupBox,
        QHeaderView,
        QLabel,
        QLineEdit,
        QListWidget,
        QMainWindow,
        QMessageBox,
        QPushButton,
        QSplitter,
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


def exec_qt(obj) -> int:
    """Führt Qt-Objekte kompatibel mit PyQt5/PySide aus.

    PyQt5 nutzt historisch ``exec_()``, neuere Bindings stellen zusätzlich
    ``exec()`` bereit. Der Helper verhindert Binding-spezifische Aufrufe in
    Dialogen und beim QApplication-Eventloop.
    """

    exec_method = getattr(obj, "exec", None) or getattr(obj, "exec_", None)
    if exec_method is None:
        raise AttributeError(f"{type(obj).__name__} besitzt weder exec() noch exec_().")
    return int(exec_method())

__all__ = [
    "exec_qt",
    "QApplication",
    "QComboBox",
    "QDate",
    "QDateEdit",
    "QDialog",
    "QFileDialog",
    "QFormLayout",
    "QHBoxLayout",
    "QGroupBox",
    "QHeaderView",
    "QLabel",
    "QLineEdit",
    "QListWidget",
    "QMainWindow",
    "QMessageBox",
    "QPushButton",
    "QSplitter",
    "QStackedWidget",
    "QTableWidget",
    "QTableWidgetItem",
    "QTextEdit",
    "QVBoxLayout",
    "QWidget",
]
