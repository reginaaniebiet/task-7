from sqlmodel import SQLModel, Field
from typing import Optional

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    stock: int

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    hashed_password: str
    is_admin: bool = False

class CartItem(SQLModel):
    product_id: int
    quantity: int
