@echo off
cd /d "%~dp0"
echo Starting all arenas...
start http://localhost:8765
start http://localhost:8765/validate.html
start http://localhost:8765/competition.html
python server.py
pause
