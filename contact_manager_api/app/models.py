from typing import Optional
from sqlmodel import SQLModel, Field, UniqueConstraint

# ---------- Users ----------

class UserBase(SQLModel):
    username: str = Field(index=True, min_length=3, max_length=50)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    __table_args__ = (UniqueConstraint("username", name="uq_user_username"),)

class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=128)

class UserRead(UserBase):
    id: int

# ---------- Contacts ----------

class ContactBase(SQLModel):
    name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=255)
    phone: str = Field(min_length=3, max_length=50)

class Contact(ContactBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)

class ContactCreate(ContactBase):
    pass

class ContactUpdate(SQLModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[str] = Field(default=None, min_length=3, max_length=255)
    phone: Optional[str] = Field(default=None, min_length=3, max_length=50)

class ContactRead(ContactBase):
    id: int
