from qt_compat import (
    exec_qt,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSplitter,
    QTableWidget,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from file_manager import open_file
from ui.common import fill_table, row_value, show_error
from ui.forms import DocumentDialog
from services.document_service import create_document, list_documents


class DocumentsView(QWidget):
    def __init__(self):
        super().__init__()
        self.rows = []

        self.search = QLineEdit()
        self.search.setPlaceholderText("Suche nach Titel, Datei, Kategorie oder Notiz")
        self.search.textChanged.connect(self.refresh)

        self.table = QTableWidget()
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.cellClicked.connect(self.show_preview)
        self.table.cellDoubleClicked.connect(self.open_doc)

        import_button = QPushButton("Dokument importieren")
        import_button.clicked.connect(self.add)

        top = QHBoxLayout()
        top.addWidget(self.search)
        top.addWidget(import_button)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.addLayout(top)
        left_layout.addWidget(self.table)

        self.preview_title = QLabel("Wählen Sie ein Dokument aus, um die Vorschau zu sehen.")
        self.preview_title.setWordWrap(True)
        self.notes = QTextEdit()
        self.notes.setReadOnly(True)
        self.notes.setPlaceholderText("Notizen")
        self.open_button = QPushButton("Ausgewählte Datei öffnen")
        self.open_button.clicked.connect(self.open_selected_doc)
        self.open_button.setEnabled(False)

        preview_group = QGroupBox("Dokumentvorschau")
        preview_layout = QVBoxLayout(preview_group)
        preview_layout.addWidget(self.preview_title)
        preview_layout.addWidget(self.notes)
        preview_layout.addWidget(self.open_button)

        splitter = QSplitter()
        splitter.addWidget(left)
        splitter.addWidget(preview_group)
        splitter.setSizes([760, 440])

        layout = QVBoxLayout(self)
        layout.addWidget(splitter)
        self.refresh()

    def add(self):
        dialog = DocumentDialog(self)
        if exec_qt(dialog):
            try:
                create_document(
                    dialog.title.text(),
                    dialog.file.text(),
                    dialog.date.date().toString("yyyy-MM-dd"),
                    dialog.category.text(),
                    dialog.case.currentData(),
                    dialog.status.currentData(),
                    dialog.notes.toPlainText(),
                )
                self.refresh()
            except Exception as exc:
                show_error(self, exc)

    def refresh(self):
        selected_id = self._selected_document_id()
        self.rows = list_documents(self.search.text())
        fill_table(self.table, ["id", "title", "original_filename", "category", "case_title", "status", "created_at"], self.rows)
        if selected_id:
            for row_index, row in enumerate(self.rows):
                if row_value(row, "id") == selected_id:
                    self.table.selectRow(row_index)
                    self.show_preview(row_index, 0)
                    return
        self.clear_preview()

    def clear_preview(self):
        self.preview_title.setText("Wählen Sie ein Dokument aus, um die Vorschau zu sehen.")
        self.notes.clear()
        self.open_button.setEnabled(False)

    def _selected_document_id(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.rows):
            return None
        return row_value(self.rows[row], "id")

    def show_preview(self, row, _column):
        if row < 0 or row >= len(self.rows):
            self.clear_preview()
            return
        doc = self.rows[row]
        self.preview_title.setText(
            f"<b>{row_value(doc, 'title')}</b><br>"
            f"Datei: {row_value(doc, 'original_filename') or '-'}<br>"
            f"Akte: {row_value(doc, 'case_title') or 'Keine Akte'} | Kategorie: {row_value(doc, 'category') or '-'}<br>"
            f"Dokumentdatum: {row_value(doc, 'document_date') or '-'} | Status: {row_value(doc, 'status') or '-'}<br>"
            f"Gespeichert unter: {row_value(doc, 'stored_path') or '-'}"
        )
        self.notes.setPlainText(row_value(doc, "notes") or "Keine Notizen hinterlegt.")
        self.open_button.setEnabled(bool(row_value(doc, "stored_path")))

    def open_selected_doc(self):
        self.open_doc(self.table.currentRow(), 0)

    def open_doc(self, row, _column):
        if row < 0 or row >= len(self.rows):
            return
        try:
            open_file(row_value(self.rows[row], "stored_path"))
        except Exception as exc:
            show_error(self, exc)
