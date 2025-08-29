from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import create_db_and_tables
from app.middleware import ip_logging_middleware
from app.settings import settings
from app.auth import router as auth_router
from app.routers.contacts import router as contacts_router

app = FastAPI(
    title="Contact Manager API",
    version="1.0.0",
    description="Contacts with per-user access control via JWT, IP logging, and CORS.",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# IP logging middleware
app.middleware("http")(ip_logging_middleware)

# Routers
app.include_router(auth_router)
app.include_router(contacts_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health", tags=["util"])
def health():
    return {"status": "ok"}
