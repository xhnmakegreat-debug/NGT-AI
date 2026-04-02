@echo off
REM Setup virtual environment and install requirements on Windows (PowerShell alternative exists)
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
echo Setup complete. You can run start.bat to start the app.
pause
