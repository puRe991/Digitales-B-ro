import sys
from qt_compat import QApplication, QMessageBox
from database import initialize_database
from ui.main_window import MainWindow


def main() -> int:
    app = QApplication(sys.argv)
    try:
        initialize_database()
    except Exception as exc:
        QMessageBox.critical(None, "Datenbankfehler", f"Die Datenbank konnte nicht initialisiert werden:\n{exc}")
        return 1
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
