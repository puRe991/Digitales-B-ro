from qt_compat import exec_qt, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from ui.common import show_error

def fill(table, headers, rows):
    table.setColumnCount(len(headers)); table.setHorizontalHeaderLabels(headers); table.setRowCount(len(rows))
    for r,row in enumerate(rows):
        for c,key in enumerate(headers): table.setItem(r,c,QTableWidgetItem(str(row.get(key, "") or "")))
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
from ui.forms import ContactDialog
from services.contact_service import create_contact, list_contacts
class ContactsView(QWidget):
    def __init__(self): super().__init__(); self.table=QTableWidget(); b=QPushButton("Neuer Kontakt"); b.clicked.connect(self.add); l=QVBoxLayout(self); l.addWidget(b); l.addWidget(self.table); self.refresh()
    def add(self):
        d=ContactDialog(self)
        if exec_qt(d):
            try: create_contact(d.name.text(), d.org.text(), d.role.text(), d.phone.text(), d.email.text(), d.addr.toPlainText(), d.notes.toPlainText()); self.refresh()
            except Exception as e: show_error(self,e)
    def refresh(self): fill(self.table,["id","name","organization","role","phone","email","created_at"],list_contacts())
