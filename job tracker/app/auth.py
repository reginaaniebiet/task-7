from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter(tags=["auth"])

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/token", response_model=Token, summary="Demo token endpoint")
async def issue_token(form: OAuth2PasswordRequestForm = Depends()):
    """
    Demo-only: we accept any password and treat the *username* as the numeric user_id.
    Returns that number as the bearer token.
    """
    try:
        int(form.username)
    except ValueError:
        raise HTTPException(status_code=400, detail="username must be a numeric user_id (e.g., '1')")
    return Token(access_token=form.username)

def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    """
    In a real app, decode and validate a JWT.
    Here, we interpret the bearer token as the integer user_id.
    """
    try:
        return int(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
