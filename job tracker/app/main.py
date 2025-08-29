from fastapi import FastAPI

from app.db import create_db_and_tables
from app.middleware import enforce_user_agent_header
from app.auth import router as auth_router
from app.routers.applications import router as applications_router

app = FastAPI(
    title="Job Application Tracker",
    version="1.0.0",
    description="Per-user Job Application Tracker with search and middleware."
)

# Middleware: reject if User-Agent header is missing
app.middleware("http")(enforce_user_agent_header)

# Routers
app.include_router(auth_router)
app.include_router(applications_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
