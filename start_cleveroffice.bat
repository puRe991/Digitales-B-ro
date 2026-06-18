@echo off
setlocal
cd /d "%~dp0"
python start_cleveroffice.py %*
if errorlevel 1 (
    echo.
    echo CleverOffice Archiv konnte nicht gestartet werden.
    pause
    exit /b 1
)
endlocal
