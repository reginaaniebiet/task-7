from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session, select

from app.db import get_session
from app.models import User, UserCreate, UserRead
from app.settings import settings

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- Password utils ----------

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ---------- JWT utils ----------

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None  # username

# ---------- Auth dependencies ----------

def get_user_by_username(session: Session, username: str) -> Optional[User]:
    return session.exec(select(User).where(User.username == username)).first()

def authenticate_user(session: Session, username: str, password: str) -> Optional[User]:
    user = get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

@router.post("/register", response_model=UserRead, status_code=201)
def register_user(payload: UserCreate, session: Session = Depends(get_session)):
    existing = get_user_by_username(session, payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username is already taken")
    user = User(username=payload.username, hashed_password=get_password_hash(payload.password))
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserRead.model_validate(user)

@router.post("/token", response_model=Token, summary="OAuth2 password flow")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.username})
    return Token(access_token=token)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(session, username)
    if user is None:
        raise credentials_exception
    return user
