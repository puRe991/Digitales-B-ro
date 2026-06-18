from PySide6.QtWidgets import QMessageBox

def show_error(parent, message: str) -> None:
    QMessageBox.critical(parent, "Fehler", str(message))
