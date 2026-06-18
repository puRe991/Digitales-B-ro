# Digitales-B-ro

## CleverOffice Archiv starten

### Windows

Doppelklicke `start_cleveroffice.bat` oder führe im Terminal aus:

```bat
start_cleveroffice.bat
```

### macOS/Linux

```bash
python start_cleveroffice.py
```

Der Starter legt bei Bedarf `cleveroffice_archiv/.venv` an, installiert die Abhängigkeiten aus `cleveroffice_archiv/requirements.txt` und startet die Anwendung.

Wenn die Umgebung bereits vorbereitet ist, kannst du die Installation überspringen:

```bash
python start_cleveroffice.py --skip-install
```
