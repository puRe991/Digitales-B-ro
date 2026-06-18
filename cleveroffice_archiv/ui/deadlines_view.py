from qt_compat import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from ui.common import show_error

def fill(table, headers, rows):
    table.setColumnCount(len(headers)); table.setHorizontalHeaderLabels(headers); table.setRowCount(len(rows))
    for r,row in enumerate(rows):
        for c,key in enumerate(headers): table.setItem(r,c,QTableWidgetItem(str(row.get(key, "") or "")))
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
from ui.forms import DeadlineDialog
from services.deadline_service import create_deadline, list_deadlines
class DeadlinesView(QWidget):
    def __init__(self): super().__init__(); self.table=QTableWidget(); b=QPushButton("Neue Frist"); b.clicked.connect(self.add); l=QVBoxLayout(self); l.addWidget(b); l.addWidget(self.table); self.refresh()
    def add(self):
        d=DeadlineDialog(self)
        if d.exec():
            try: create_deadline(d.title.text(), d.due.date().toString("yyyy-MM-dd"), d.rem.date().toString("yyyy-MM-dd"), d.status.currentData(), d.case.currentData()); self.refresh()
            except Exception as e: show_error(self,e)
    def refresh(self): fill(self.table,["id","title","due_date","reminder_date","status","case_title","document_title","created_at"],list_deadlines())
