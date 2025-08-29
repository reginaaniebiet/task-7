from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db import create_db_and_tables
from app.middleware import request_counter_middleware
from app.routers.notes import router as notes_router

app = FastAPI(title="Notes API", version="1.0")

# CORS setup
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware
app.middleware("http")(request_counter_middleware)

# Routers
app.include_router(notes_router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
