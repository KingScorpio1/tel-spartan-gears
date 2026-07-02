@echo off
cd /d "%~dp0"
echo Starting competition arena at http://localhost:8765/competition.html
start http://localhost:8765/competition.html
python server.py
pause
