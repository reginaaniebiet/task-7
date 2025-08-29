from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import Session, select
from app.models import Product
from app.database import get_session
from app.auth import get_current_admin_user

router = APIRouter(prefix="/admin/products", tags=["products"])

@router.post("/", response_model=Product)
def create_product(product: Product, session: Session = Depends(get_session), admin=Depends(get_current_admin_user)):
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@router.get("/", response_model=List[Product], tags=["products"])
def list_products(session: Session = Depends(get_session)):
    products = session.exec(select(Product)).all()
    return products
