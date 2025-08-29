import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.db import get_session
from app.models import Note, NoteCreate, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])

BACKUP_FILE = "notes.json"

def save_backup(session: Session):
    notes = session.exec(select(Note)).all()
    with open(BACKUP_FILE, "w", encoding="utf-8") as f:
        json.dump([note.model_dump() for note in notes], f, indent=2, default=str)

@router.post("/", response_model=NoteRead, status_code=201)
def create_note(note: NoteCreate, session: Session = Depends(get_session)):
    new_note = Note(**note.model_dump())
    session.add(new_note)
    session.commit()
    session.refresh(new_note)
    save_backup(session)
    return new_note

@router.get("/", response_model=List[NoteRead])
def list_notes(session: Session = Depends(get_session)):
    return session.exec(select(Note)).all()

@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{note_id}", status_code=204)
def delete_note(note_id: int, session: Session = Depends(get_session)):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    session.delete(note)
    session.commit()
    save_backup(session)
    return None
