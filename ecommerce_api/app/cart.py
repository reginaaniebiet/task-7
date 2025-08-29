from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from app.models import Product, CartItem
from app.database import get_session
from app.auth import get_current_active_user
import json
from pathlib import Path

router = APIRouter(prefix="/cart", tags=["cart"])

# Simple in-memory cart storage per user (for demo; not persistent)
# In real apps, use DB or Redis for carts
user_carts = {}

def save_order(order_data: dict):
    orders_file = Path("app/orders.json")
    if orders_file.exists():
        with orders_file.open("r") as f:
            orders = json.load(f)
    else:
        orders = []
    orders.append(order_data)
    with orders_file.open("w") as f:
        json.dump(orders, f, indent=4)

@router.post("/add/")
def add_to_cart(item: CartItem, current_user = Depends(get_current_active_user)):
    cart = user_carts.setdefault(current_user.username, [])
    # Check stock before adding
    from app.database import engine
    with Session(engine) as session:
        product = session.get(Product, item.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail="Not enough stock")
    # Add to cart or update quantity
    for cart_item in cart:
        if cart_item.product_id == item.product_id:
            cart_item.quantity += item.quantity
            break
    else:
        cart.append(item)
    return {"msg": "Added to cart", "cart": cart}

@router.post("/checkout/")
def checkout(current_user = Depends(get_current_active_user)):
    cart = user_carts.get(current_user.username)
    if not cart or len(cart) == 0:
        raise HTTPException(status_code=400, detail="Cart is empty")

    from app.database import engine
    total = 0
    with Session(engine) as session:
        # Verify stock & update
        for item in cart:
            product = session.get(Product, item.product_id)
            if not product or product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name if product else 'unknown product'}")
        for item in cart:
            product = session.get(Product, item.product_id)
            product.stock -= item.quantity
            session.add(product)
            total += product.price * item.quantity
        session.commit()

    order_data = {
        "user": current_user.username,
        "items": [{"product_id": i.product_id, "quantity": i.quantity} for i in cart],
        "total": total,
        "timestamp": datetime.utcnow().isoformat()
    }
    save_order(order_data)
    user_carts[current_user.username] = []  # Clear cart

    return {"msg": "Order placed successfully", "order": order_data}
