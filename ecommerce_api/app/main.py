from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.middleware import add_process_time_header
from app.users import router as users_router
from app.products import router as products_router
from app.cart import router as cart_router

app = FastAPI(title="E-Commerce API")

# Middleware
app.middleware("http")(add_process_time_header)

# CORS (allow localhost frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(products_router)
app.include_router(cart_router)

@app.on_event("startup")
def on_startup():
    init_db()
