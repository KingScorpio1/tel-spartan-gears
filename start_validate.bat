@echo off
cd /d "%~dp0"
echo Starting Validation Arena at http://localhost:8765/validate.html
start http://localhost:8765/validate.html
python server.py
pause
