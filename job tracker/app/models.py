from datetime import date
from enum import Enum
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.types import Enum as SAEnum
from sqlmodel import SQLModel, Field


class StatusEnum(str, Enum):
    pending = "pending"
    interview = "interview"
    rejected = "rejected"
    accepted = "accepted"


class JobApplicationBase(SQLModel):
    company: str = Field(min_length=1, max_length=255)
    position: str = Field(min_length=1, max_length=255)
    # Persist as a proper SQL ENUM for safety
    status: StatusEnum = Field(
        sa_column=Column(SAEnum(StatusEnum, name="status_enum"), nullable=False)
    )
    date_applied: date = Field(default_factory=date.today)


class JobApplication(JobApplicationBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)


class JobApplicationCreate(JobApplicationBase):
    """Incoming payload for creating an application (user_id inferred from token)."""
    pass


class JobApplicationRead(JobApplicationBase):
    id: int
