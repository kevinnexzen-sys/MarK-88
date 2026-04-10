@echo off
start cmd /k "cd /d %~dp0..\backend && uvicorn app.main:app --host 0.0.0.0 --port 8787"
start cmd /k "cd /d %~dp0..\desktop_worker && python worker.py"
start cmd /k "cd /d %~dp0..\pc_agent && python claw_pc_agent.py"
