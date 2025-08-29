from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.models import User
from app.auth import get_password_hash, authenticate_user, create_access_token
from app.database import get_session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", status_code=201)
def register_user(username: str, password: str, session: Session = Depends(get_session)):
    existing_user = session.exec(User.select().where(User.username == username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    user = User(
        username=username,
        hashed_password=get_password_hash(password),
        is_admin=False
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"msg": "User created successfully"}

@router.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
