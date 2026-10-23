@echo off
cd /d "%~dp0"
call .venv\Scripts\activate.bat
echo === Running tests ===
python -m pytest
echo.
echo === Starting server: open http://127.0.0.1:8000/ ===
python manage.py runserver
pause
