@echo off
setlocal
cd /d "%~dp0"

echo ============================================
echo DentPanX-AI
echo Installation and startup
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
    echo ERROR: Python was not found.
    echo Install Python 3.10 or 3.11 and select
    echo "Add Python to PATH" during installation.
    pause
    exit /b 1
)

echo Installing required Python packages...
python -m pip install --upgrade pip
if errorlevel 1 goto :error

python -m pip install -r requirements.txt
if errorlevel 1 goto :error

echo.
echo Starting the application...
python -m streamlit run app.py

if errorlevel 1 goto :error
exit /b 0

:error
echo.
echo The application could not be started.
echo Review the error messages above.
pause
exit /b 1
