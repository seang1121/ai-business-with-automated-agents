@echo off
echo ============================================================
echo   AI Business with Automated Agents — Starting...
echo ============================================================

:: Create venv if missing
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate venv
call venv\Scripts\activate

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt -q

:: Seed demo data if DB doesn't exist
if not exist "business.db" (
    echo Seeding demo data...
    python backend/seed_demo.py
)

:: Start Flask
echo.
echo Starting server...
python backend/app.py
