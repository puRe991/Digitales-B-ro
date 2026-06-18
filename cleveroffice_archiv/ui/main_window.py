from PySide6.QtWidgets import QMainWindow, QListWidget, QStackedWidget, QWidget, QHBoxLayout
from ui.cases_view import CasesView
from ui.contacts_view import ContactsView
from ui.dashboard_view import DashboardView
from ui.deadlines_view import DeadlinesView
from ui.documents_view import DocumentsView
from ui.tasks_view import TasksView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CleverOffice Archiv")
        self.resize(1200, 760)
        self.nav = QListWidget(); self.nav.setFixedWidth(190)
        self.stack = QStackedWidget()
        self.documents = DocumentsView(); self.cases = CasesView(); self.tasks = TasksView(); self.deadlines = DeadlinesView(); self.contacts = ContactsView()
        self.dashboard = DashboardView({
            "Dokument importieren": self.documents.add,
            "Neue Akte": self.cases.add,
            "Neue Aufgabe": self.tasks.add,
            "Neue Frist": self.deadlines.add,
        })
        views = [("Dashboard", self.dashboard), ("Dokumente", self.documents), ("Akten", self.cases), ("Aufgaben", self.tasks), ("Fristen", self.deadlines), ("Kontakte", self.contacts)]
        for name, view in views:
            self.nav.addItem(name); self.stack.addWidget(view)
        self.nav.currentRowChanged.connect(self._switch)
        root = QWidget(); layout = QHBoxLayout(root); layout.addWidget(self.nav); layout.addWidget(self.stack, 1)
        self.setCentralWidget(root); self.nav.setCurrentRow(0)
        self.setStyleSheet("QPushButton{padding:7px 12px;} QLineEdit,QComboBox,QDateEdit{padding:5px;} QTableWidget{gridline-color:#ddd;}")

    def _switch(self, index):
        self.stack.setCurrentIndex(index)
        widget = self.stack.currentWidget()
        if hasattr(widget, "refresh"):
            widget.refresh()
