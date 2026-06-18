from PySide6.QtCore import QDate
from PySide6.QtWidgets import (QComboBox, QDateEdit, QDialog, QFileDialog, QFormLayout,
                               QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QVBoxLayout)
from services.case_service import case_options


def combo(items):
    c = QComboBox()
    for value, label in items:
        c.addItem(label, value)
    return c


class BaseDialog(QDialog):
    def buttons(self, layout):
        row = QHBoxLayout(); row.addStretch()
        ok = QPushButton("Speichern"); cancel = QPushButton("Abbrechen")
        ok.clicked.connect(self.accept); cancel.clicked.connect(self.reject)
        row.addWidget(ok); row.addWidget(cancel); layout.addLayout(row)


class CaseDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Neue Akte")
        self.title=QLineEdit(); self.desc=QTextEdit(); self.type=combo([(x,x) for x in ["Privat","Firma","Verein/Feuerwehr","Sonstiges"]]); self.status=combo([(x,x) for x in ["aktiv","abgeschlossen","archiviert"]])
        form=QFormLayout(); form.addRow("Titel*", self.title); form.addRow("Beschreibung", self.desc); form.addRow("Typ", self.type); form.addRow("Status", self.status)
        lay=QVBoxLayout(self); lay.addLayout(form); self.buttons(lay)


class DocumentDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Dokument importieren")
        self.file=QLineEdit(); browse=QPushButton("Auswählen…"); browse.clicked.connect(self.pick)
        fr=QHBoxLayout(); fr.addWidget(self.file); fr.addWidget(browse)
        self.title=QLineEdit(); self.date=QDateEdit(calendarPopup=True); self.date.setDisplayFormat("yyyy-MM-dd"); self.date.setDate(QDate.currentDate())
        self.category=QLineEdit(); self.case=combo(case_options()); self.status=combo([(x,x) for x in ["offen","erledigt","archiviert"]]); self.notes=QTextEdit()
        form=QFormLayout(); form.addRow("Datei*", fr); form.addRow("Titel*", self.title); form.addRow("Dokumentdatum", self.date); form.addRow("Kategorie", self.category); form.addRow("Akte", self.case); form.addRow("Status", self.status); form.addRow("Notiz", self.notes)
        lay=QVBoxLayout(self); lay.addLayout(form); self.buttons(lay)
    def pick(self):
        path,_=QFileDialog.getOpenFileName(self,"Datei importieren")
        if path:
            self.file.setText(path)
            if not self.title.text(): self.title.setText(path.split('/')[-1])


class TaskDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Neue Aufgabe")
        self.title=QLineEdit(); self.desc=QTextEdit(); self.due=QDateEdit(calendarPopup=True); self.due.setDisplayFormat("yyyy-MM-dd"); self.due.setDate(QDate.currentDate())
        self.status=combo([(x,x) for x in ["offen","in Bearbeitung","erledigt"]]); self.case=combo(case_options())
        form=QFormLayout(); form.addRow("Titel*", self.title); form.addRow("Beschreibung", self.desc); form.addRow("Fällig am", self.due); form.addRow("Status", self.status); form.addRow("Akte", self.case)
        lay=QVBoxLayout(self); lay.addLayout(form); self.buttons(lay)


class DeadlineDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Neue Frist")
        self.title=QLineEdit(); self.due=QDateEdit(calendarPopup=True); self.due.setDisplayFormat("yyyy-MM-dd"); self.due.setDate(QDate.currentDate())
        self.rem=QDateEdit(calendarPopup=True); self.rem.setDisplayFormat("yyyy-MM-dd"); self.rem.setDate(QDate.currentDate())
        self.status=combo([(x,x) for x in ["offen","erledigt"]]); self.case=combo(case_options())
        form=QFormLayout(); form.addRow("Titel*", self.title); form.addRow("Fällig am*", self.due); form.addRow("Erinnerung", self.rem); form.addRow("Status", self.status); form.addRow("Akte", self.case)
        lay=QVBoxLayout(self); lay.addLayout(form); self.buttons(lay)


class ContactDialog(BaseDialog):
    def __init__(self, parent=None):
        super().__init__(parent); self.setWindowTitle("Neuer Kontakt")
        self.name=QLineEdit(); self.org=QLineEdit(); self.role=QLineEdit(); self.phone=QLineEdit(); self.email=QLineEdit(); self.addr=QTextEdit(); self.notes=QTextEdit()
        form=QFormLayout(); form.addRow("Name*", self.name); form.addRow("Organisation", self.org); form.addRow("Rolle", self.role); form.addRow("Telefon", self.phone); form.addRow("E-Mail", self.email); form.addRow("Adresse", self.addr); form.addRow("Notiz", self.notes)
        lay=QVBoxLayout(self); lay.addLayout(form); self.buttons(lay)
