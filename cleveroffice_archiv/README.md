# CleverOffice Archiv

Lokale Windows-Desktop-Anwendung zur Offline-Verwaltung von Dokumenten, Akten, Aufgaben, Fristen und Kontakten.

## Installation

```bash
cd cleveroffice_archiv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Hinweis für 32-Bit-Windows: Das Projekt nutzt PyQt5, weil PySide6 keine passenden 32-Bit-Windows-Wheels veröffentlicht. Wenn die virtuelle Umgebung mit einer falschen Python-Version erstellt wurde, lösche `.venv` und führe die Installation erneut aus.

## Spätere Ausbaustufen

- OCR für gescannte Dokumente
- KI-gestützte Dokumentenerkennung und automatische Kategorisierung
- PDF-Zusammenführen und Seitenverwaltung
- Benutzerrollen und Rechteverwaltung
- Optionale Verschlüsselung sensibler Ablagen
- Netzwerk- oder Mehrplatzbetrieb

Diese Funktionen sind bewusst nicht Teil des MVP 1.0, damit die lokale Basis stabil und wartbar bleibt.
