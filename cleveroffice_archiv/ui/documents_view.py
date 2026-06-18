from qt_compat import exec_qt, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget
from ui.common import fill_table, show_error

from qt_compat import QLineEdit
from file_manager import open_file
from ui.forms import DocumentDialog
from services.document_service import create_document, list_documents
class DocumentsView(QWidget):
    def __init__(self):
        super().__init__(); self.search=QLineEdit(); self.search.setPlaceholderText("Suche nach Titel, Datei, Kategorie oder Notiz"); self.search.textChanged.connect(self.refresh); self.table=QTableWidget(); self.table.cellDoubleClicked.connect(self.open_doc); b=QPushButton("Dokument importieren"); b.clicked.connect(self.add); top=QHBoxLayout(); top.addWidget(self.search); top.addWidget(b); l=QVBoxLayout(self); l.addLayout(top); l.addWidget(self.table); self.refresh()
    def add(self):
        d=DocumentDialog(self)
        if exec_qt(d):
            try: create_document(d.title.text(), d.file.text(), d.date.date().toString("yyyy-MM-dd"), d.category.text(), d.case.currentData(), d.status.currentData(), d.notes.toPlainText()); self.refresh()
            except Exception as e: show_error(self,e)
    def refresh(self): self.rows=list_documents(self.search.text()); fill_table(self.table,["id","title","original_filename","category","case_title","status","created_at"],self.rows)
    def open_doc(self,row,col):
        try: open_file(self.rows[row]["stored_path"])
        except Exception as e: show_error(self,e)
