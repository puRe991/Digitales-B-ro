from qt_compat import exec_qt, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from ui.common import show_error

def fill(table, headers, rows):
    table.setColumnCount(len(headers)); table.setHorizontalHeaderLabels(headers); table.setRowCount(len(rows))
    for r,row in enumerate(rows):
        for c,key in enumerate(headers): table.setItem(r,c,QTableWidgetItem(str(row.get(key, "") or "")))
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
from ui.forms import CaseDialog
from services.case_service import create_case, list_cases
class CasesView(QWidget):
    def __init__(self): super().__init__(); self.table=QTableWidget(); b=QPushButton("Neue Akte"); b.clicked.connect(self.add); l=QVBoxLayout(self); l.addWidget(b); l.addWidget(self.table); self.refresh()
    def add(self):
        d=CaseDialog(self)
        if exec_qt(d):
            try: create_case(d.title.text(), d.desc.toPlainText(), d.type.currentData(), d.status.currentData()); self.refresh()
            except Exception as e: show_error(self,e)
    def refresh(self): fill(self.table,["id","title","case_type","status","created_at"],list_cases())
