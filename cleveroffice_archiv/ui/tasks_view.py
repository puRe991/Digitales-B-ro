from qt_compat import exec_qt, QWidget, QVBoxLayout, QPushButton, QTableWidget
from ui.common import fill_table, show_error

from ui.forms import TaskDialog
from services.task_service import create_task, list_tasks
class TasksView(QWidget):
    def __init__(self): super().__init__(); self.table=QTableWidget(); b=QPushButton("Neue Aufgabe"); b.clicked.connect(self.add); l=QVBoxLayout(self); l.addWidget(b); l.addWidget(self.table); self.refresh()
    def add(self):
        d=TaskDialog(self)
        if exec_qt(d):
            try: create_task(d.title.text(), d.desc.toPlainText(), d.due.date().toString("yyyy-MM-dd"), d.status.currentData(), d.case.currentData()); self.refresh()
            except Exception as e: show_error(self,e)
    def refresh(self): fill_table(self.table,["id","title","due_date","status","case_title","document_title","created_at"],list_tasks())
