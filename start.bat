@echo off
cd /d "%~dp0"
echo Starting custom server at http://localhost:8765
start http://localhost:8765
python server.py
pause
