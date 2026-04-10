# MARK v8.1 Full System

Cloud-first AI operations platform combining MARK Cloud, CLAW Android app, Desktop Worker, Windows PC Agent, Chrome extension, learning system, provider routing, approvals, and remote PC control.

## Included layers
- `backend/`: FastAPI backend, agent fabric, task queue, approvals, settings-first setup
- `claw-agent/`: Flutter Android app scaffold with dashboard, approvals, preview, memory/skills/knowledge, voice-first mobile UX
- `desktop_worker/`: local browser/WhatsApp/local-watch worker
- `pc_agent/`: silent Windows PC agent
- `extension/`: Chrome extension for WhatsApp Web
- `scripts/`: Windows/startup/install helpers and GitHub push helper
- `docs/`: setup, deployment, BIOS/network, provider mode guidance

## Quick start
1. Install Python 3.11+
2. `cd backend`
3. `pip install -r requirements.txt`
4. `uvicorn app.main:app --host 0.0.0.0 --port 8787 --reload`
5. Open `http://localhost:8787`
6. Default users:
   - admin / admin123
   - manager / manager123
   - approver / approver123

## Capability status
This repo is a substantial full-stack foundation with real runnable backend, worker registration, settings-first setup, task queue, approvals, provider routing skeleton, learning-event pipeline, and mobile/worker/app scaffolding. Real external accounts and deployment are still required for Google/Supabase/WhatsApp/voice-quality providers.
