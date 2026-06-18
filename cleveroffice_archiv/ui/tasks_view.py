from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from ui.common import show_error

def fill(table, headers, rows):
    table.setColumnCount(len(headers)); table.setHorizontalHeaderLabels(headers); table.setRowCount(len(rows))
    for r,row in enumerate(rows):
        for c,key in enumerate(headers): table.setItem(r,c,QTableWidgetItem(str(row.get(key, "") or "")))
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
from ui.forms import TaskDialog
from services.task_service import create_task, list_tasks
class TasksView(QWidget):
    def __init__(self): super().__init__(); self.table=QTableWidget(); b=QPushButton("Neue Aufgabe"); b.clicked.connect(self.add); l=QVBoxLayout(self); l.addWidget(b); l.addWidget(self.table); self.refresh()
    def add(self):
        d=TaskDialog(self)
        if d.exec():
            try: create_task(d.title.text(), d.desc.toPlainText(), d.due.date().toString("yyyy-MM-dd"), d.status.currentData(), d.case.currentData()); self.refresh()
            except Exception as e: show_error(self,e)
    def refresh(self): fill(self.table,["id","title","due_date","status","case_title","document_title","created_at"],list_tasks())
