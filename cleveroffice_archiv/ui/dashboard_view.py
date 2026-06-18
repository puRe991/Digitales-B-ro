from qt_compat import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTableWidget
from services.deadline_service import list_deadlines
from services.task_service import list_tasks
from services.document_service import recent_documents
from ui.common import fill_table


class DashboardView(QWidget):
    def __init__(self, actions: dict):
        super().__init__()
        layout = QVBoxLayout(self)
        buttons = QHBoxLayout()
        for text, callback in actions.items():
            button = QPushButton(text)
            button.clicked.connect(callback)
            buttons.addWidget(button)
        layout.addLayout(buttons)
        self.deadlines = QTableWidget(); self.tasks = QTableWidget(); self.docs = QTableWidget()
        layout.addWidget(QLabel("Offene Fristen")); layout.addWidget(self.deadlines)
        layout.addWidget(QLabel("Offene Aufgaben")); layout.addWidget(self.tasks)
        layout.addWidget(QLabel("Zuletzt importierte Dokumente")); layout.addWidget(self.docs)
        self.refresh()

    def refresh(self):
        fill_table(self.deadlines, ["id", "title", "due_date", "status", "case_title"], list_deadlines(True, 8))
        fill_table(self.tasks, ["id", "title", "due_date", "status", "case_title"], list_tasks(True, 8))
        fill_table(self.docs, ["id", "title", "original_filename", "category", "created_at"], recent_documents(8))
