from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.models import Contact, ContactCreate, ContactUpdate, ContactRead
from app.auth import get_current_user, User

router = APIRouter(prefix="/contacts", tags=["contacts"])

def ensure_owner_or_404(session: Session, contact_id: int, user: User) -> Contact:
    contact = session.get(Contact, contact_id)
    if not contact or contact.user_id != user.id:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@router.post("/", response_model=ContactRead, status_code=201)
def create_contact(
    payload: ContactCreate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    contact = Contact(**payload.model_dump(), user_id=user.id)
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact

@router.get("/", response_model=List[ContactRead])
def list_contacts(
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    stmt = select(Contact).where(Contact.user_id == user.id).order_by(Contact.id.desc())
    return session.exec(stmt).all()

@router.put("/{contact_id}", response_model=ContactRead)
def update_contact(
    contact_id: int,
    payload: ContactUpdate,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    contact = ensure_owner_or_404(session, contact_id, user)
    data = payload.model_dump(exclude_unset=True)
    for k, v in data.items():
        setattr(contact, k, v)
    session.add(contact)
    session.commit()
    session.refresh(contact)
    return contact

@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(
    contact_id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
):
    contact = ensure_owner_or_404(session, contact_id, user)
    session.delete(contact)
    session.commit()
    return None
