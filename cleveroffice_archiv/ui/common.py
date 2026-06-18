from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from qt_compat import QHeaderView, QMessageBox, QTableWidget, QTableWidgetItem


def show_error(parent, message: object) -> None:
    QMessageBox.critical(parent, "Fehler", str(message))


def row_value(row: Any, key: str) -> Any:
    """Return a value from sqlite rows, mappings or plain objects.

    sqlite3.Row deliberately does not implement ``dict.get``. Centralising the
    access prevents table refresh crashes when service results are rendered.
    """
    if isinstance(row, Mapping):
        return row.get(key, "")
    try:
        return row[key]
    except (IndexError, KeyError, TypeError):
        return getattr(row, key, "")


def fill_table(table: QTableWidget, headers: Sequence[str], rows: Sequence[Any]) -> None:
    table.setSortingEnabled(False)
    table.clear()
    table.setColumnCount(len(headers))
    table.setHorizontalHeaderLabels(list(headers))
    table.setRowCount(len(rows))

    for row_index, row in enumerate(rows):
        for column_index, key in enumerate(headers):
            value = row_value(row, key)
            table.setItem(row_index, column_index, QTableWidgetItem(str(value or "")))

    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.setSortingEnabled(True)
