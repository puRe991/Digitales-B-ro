# Digitales-B-ro

## CleverOffice Archiv starten

### Windows

Doppelklicke `start_cleveroffice.bat` oder führe im Terminal aus:

```bat
start_cleveroffice.bat
```

Der Starter funktioniert auch mit 32-Bit-Windows/Python. Die Oberfläche nutzt deshalb PyQt5 statt PySide6, weil PySide6 keine passenden 32-Bit-Windows-Pakete bereitstellt.

### macOS/Linux

```bash
python start_cleveroffice.py
```

Der Starter legt bei Bedarf `cleveroffice_archiv/.venv` an, installiert die Abhängigkeiten aus `cleveroffice_archiv/requirements.txt` und startet die Anwendung.

Wenn die Umgebung bereits vorbereitet ist, kannst du die Installation überspringen:

```bash
python start_cleveroffice.py --skip-install
```

### Fehlerbehebung

Wenn die Installation nach einem Python-Wechsel weiterhin fehlschlägt, lösche den Ordner `cleveroffice_archiv/.venv` und starte erneut. Der Starter erstellt die Umgebung dann mit dem aktuell gefundenen Python neu.
