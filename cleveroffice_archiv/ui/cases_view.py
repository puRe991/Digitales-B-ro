from qt_compat import (
    exec_qt,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from file_manager import open_file
from ui.common import fill_table, row_value, show_error
from ui.forms import CaseDialog
from services.case_service import case_overview, create_case, list_cases


class CasesView(QWidget):
    def __init__(self):
        super().__init__()
        self.rows = []
        self.document_rows = []

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.cellClicked.connect(self.show_case_preview)
        self.table.cellDoubleClicked.connect(self.show_case_preview)

        add_button = QPushButton("Neue Akte")
        add_button.clicked.connect(self.add)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(add_button)
        left_layout.addWidget(self.table)

        self.summary = QLabel("Wählen Sie eine Akte aus, um die Vorschau zu sehen.")
        self.summary.setWordWrap(True)
        self.description = QTextEdit()
        self.description.setReadOnly(True)
        self.description.setPlaceholderText("Beschreibung")

        self.documents_table = QTableWidget()
        self.documents_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.documents_table.cellDoubleClicked.connect(self.open_document)

        self.tasks_table = QTableWidget()
        self.tasks_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.deadlines_table = QTableWidget()
        self.deadlines_table.setSelectionBehavior(QTableWidget.SelectRows)

        preview = QWidget()
        preview_layout = QVBoxLayout(preview)
        preview_layout.addWidget(self.summary)
        preview_layout.addWidget(self.description)
        preview_layout.addWidget(self._group("Dokumente der Akte (Doppelklick öffnet Datei)", self.documents_table))
        preview_layout.addWidget(self._group("Aufgaben", self.tasks_table))
        preview_layout.addWidget(self._group("Fristen", self.deadlines_table))

        splitter = QSplitter()
        splitter.addWidget(left)
        splitter.addWidget(preview)
        splitter.setSizes([520, 680])

        layout = QHBoxLayout(self)
        layout.addWidget(splitter)
        self.refresh()

    def _group(self, title, widget):
        group = QGroupBox(title)
        layout = QVBoxLayout(group)
        layout.addWidget(widget)
        return group

    def add(self):
        dialog = CaseDialog(self)
        if exec_qt(dialog):
            try:
                create_case(dialog.title.text(), dialog.desc.toPlainText(), dialog.type.currentData(), dialog.status.currentData())
                self.refresh()
            except Exception as exc:
                show_error(self, exc)

    def refresh(self):
        selected_id = self._selected_case_id()
        self.rows = list_cases()
        fill_table(self.table, ["id", "title", "case_type", "status", "created_at"], self.rows)
        if selected_id:
            for row_index, row in enumerate(self.rows):
                if row_value(row, "id") == selected_id:
                    self.table.selectRow(row_index)
                    self.show_case_preview(row_index, 0)
                    return
        self.clear_preview()

    def clear_preview(self):
        self.document_rows = []
        self.summary.setText("Wählen Sie eine Akte aus, um die Vorschau zu sehen.")
        self.description.clear()
        fill_table(self.documents_table, ["id", "title", "original_filename", "status"], [])
        fill_table(self.tasks_table, ["id", "title", "due_date", "status", "document_title"], [])
        fill_table(self.deadlines_table, ["id", "title", "due_date", "status", "document_title"], [])

    def _selected_case_id(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.rows):
            return None
        return row_value(self.rows[row], "id")

    def show_case_preview(self, row, _column):
        if row < 0 or row >= len(self.rows):
            self.clear_preview()
            return
        try:
            overview = case_overview(row_value(self.rows[row], "id"))
            if overview is None:
                self.clear_preview()
                return
            case = overview["case"]
            documents = overview["documents"]
            tasks = overview["tasks"]
            deadlines = overview["deadlines"]
            self.document_rows = documents
            self.summary.setText(
                f"<b>{row_value(case, 'title')}</b><br>"
                f"Typ: {row_value(case, 'case_type') or '-'} | Status: {row_value(case, 'status') or '-'} | "
                f"Erstellt: {row_value(case, 'created_at') or '-'}<br>"
                f"Dokumente: {len(documents)} | Aufgaben: {len(tasks)} | Fristen: {len(deadlines)}"
            )
            self.description.setPlainText(row_value(case, "description") or "Keine Beschreibung hinterlegt.")
            fill_table(self.documents_table, ["id", "title", "original_filename", "category", "status", "created_at"], documents)
            fill_table(self.tasks_table, ["id", "title", "due_date", "status", "document_title"], tasks)
            fill_table(self.deadlines_table, ["id", "title", "due_date", "status", "document_title"], deadlines)
        except Exception as exc:
            show_error(self, exc)

    def open_document(self, row, _column):
        if row < 0 or row >= len(self.document_rows):
            return
        try:
            open_file(row_value(self.document_rows[row], "stored_path"))
        except Exception as exc:
            show_error(self, exc)
