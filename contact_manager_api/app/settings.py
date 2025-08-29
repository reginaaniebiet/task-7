import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    # JWT
    SECRET_KEY: str = Field(default=os.getenv("SECRET_KEY", "dev-secret-change-me"))
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    # DB
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./contacts.db")

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:5500",
    ]

settings = Settings()
