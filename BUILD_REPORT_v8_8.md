# BUILD REPORT v8.8

## Added
- planner-created child tasks for complex requests
- autonomy loop respects child task completion before parent execution
- mobile/desktop learning event aliases
- stronger command interpretation including work order automation placeholder
- stronger WhatsApp bridge helpers
- extension inbound intake + outbound send support scaffold
- worker command handling emits learning events and supports richer payloads
- mobile app API adds memory + mobile event ingestion

## Validation target
- compile backend/worker/pc agent
- smoke: login, create task with child tasks, mobile event, whatsapp intake, runtime tick
