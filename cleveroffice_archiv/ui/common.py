from qt_compat import QMessageBox

def show_error(parent, message: str) -> None:
    QMessageBox.critical(parent, "Fehler", str(message))
