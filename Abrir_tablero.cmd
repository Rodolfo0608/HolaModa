@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Primero prepara el entorno siguiendo README.md.
    pause
    exit /b 1
)
echo Abre http://127.0.0.1:5000 en el navegador.
echo Mantener esta ventana abierta. Para detener, presiona Ctrl+C.
".venv\Scripts\python.exe" app.py
pause
