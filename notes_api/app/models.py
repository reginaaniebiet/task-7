from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class NoteBase(SQLModel):
    title: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int
