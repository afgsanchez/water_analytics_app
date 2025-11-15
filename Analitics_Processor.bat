@echo off
cd /d "%~dp0"

REM Activar entorno virtual
call ".venv\Scripts\activate.bat"

REM Ejecutar el main
python src\main.py

pause