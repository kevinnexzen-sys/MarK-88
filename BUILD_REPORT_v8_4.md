# BUILD REPORT v8.4

## Added
- Real integration runner for cloud task actions
- Google Sheets upsert implementation using service account JSON from dashboard settings
- Google Calendar event creation implementation using service account JSON from dashboard settings
- SMTP-based email send implementation using dashboard settings
- Integration API routes including WhatsApp worker queue endpoint
- Stronger desktop worker runtime for browser_open and whatsapp_send commands
- Stronger PC agent runtime including PowerShell command execution path
- Device control helper with smart plug + WOL wake flow
- Task action_type/action_payload storage

## Notes
- Existing shipped DB files should be removed before first run of this package to pick up new schema cleanly.
- Google actions require valid settings entered from the dashboard.
- WhatsApp send path opens the WhatsApp Web send URL on the desktop worker machine.

## Validation
- Python compileall passed for backend/app, desktop_worker, pc_agent
- Backend smoke flow passed for login, task creation, cloud execution, worker registration, WhatsApp queue, worker command polling
