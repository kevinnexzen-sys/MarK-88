# Phase 1 Setup

## Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8787 --reload
```

## Dashboard
Open http://localhost:8787

Default users:
- admin / admin123
- manager / manager123
- approver / approver123

## Desktop Worker
```bash
cd desktop_worker
python worker.py
```

## PC Agent
```bash
cd pc_agent
python claw_pc_agent.py
```
