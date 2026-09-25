@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found.
    pause
    exit /b 1
)

python -m streamlit run app.py

if errorlevel 1 (
    echo.
    echo The application could not be started.
    echo Run install_and_run_windows.bat first.
    pause
)
