from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db, SessionLocal
from .bootstrap import seed_defaults
from .api.auth_routes import router as auth_router
from .api.settings_routes import router as settings_router
from .api.task_routes import router as task_router
from .api.worker_routes import router as worker_router
from .api.device_routes import router as device_router
from .api.dashboard_routes import router as dashboard_router
from .api.health_routes import router as health_router
from .api.learning_routes import router as learning_router
from .api.integration_routes import router as integration_router
from .api.voice_routes import router as voice_router
from .api.agent_routes import router as agent_router
from .api.provider_routes import router as provider_router_api
from .api.command_routes import router as command_router
from .api.runtime_routes import router as runtime_api_router

from .api.approval_routes import router as approval_router
from .api.memory_routes import router as memory_router
from .api.device_runtime_routes import router as runtime_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_defaults(db)
    finally:
        db.close()
    yield

app = FastAPI(title="MARK v8.2", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(settings_router)
app.include_router(task_router)
app.include_router(worker_router)
app.include_router(device_router)
app.include_router(dashboard_router)
app.include_router(health_router)
app.include_router(learning_router)
app.include_router(integration_router)
app.include_router(voice_router)
app.include_router(agent_router)
app.include_router(provider_router_api)
app.include_router(command_router)
app.include_router(runtime_api_router)
app.include_router(approval_router)
app.include_router(memory_router)
app.include_router(runtime_router)

ui_dir = Path(__file__).resolve().parent.parent / "ui"
app.mount("/", StaticFiles(directory=str(ui_dir), html=True), name="ui")
