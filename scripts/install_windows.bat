@echo off
echo Installing MARK Windows startup tasks...
schtasks /create /sc onlogon /tn "MARK Backend" /tr "cmd /c cd /d %~dp0..\backend && uvicorn app.main:app --host 0.0.0.0 --port 8787" /f
schtasks /create /sc onlogon /tn "MARK Desktop Worker" /tr "cmd /c cd /d %~dp0..\desktop_worker && python worker.py" /f
schtasks /create /sc onlogon /tn "MARK PC Agent" /tr "cmd /c cd /d %~dp0..\pc_agent && pythonw claw_pc_agent.py" /f
echo Done.
