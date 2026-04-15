from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.order import Order, OrderItem
from app.models.product import Product

from app.services.ws_manager import manager
from app.services.order_worker import process_order
from app.services.notification_service import create_notification
import asyncio

VALID_TRANSITIONS = {
    "created": ["confirmed"],
    "confirmed": ["processing"],
    "processing": ["shipped"],
    "shipped": ["delivered"],
    "delivered": []
}



def create_order(db: Session, user_id: int, items_data, idempotency_key = None, background_tasks = None):

    if not items_data or len(items_data) == 0:
        raise HTTPException(status_code=400,detail="Cart is empty")
    
    existing_order = None 
    
    if idempotency_key:
        existing_order = db.query(Order)\
        .filter(Order.idempotency_key == idempotency_key)\
        .first()

    if existing_order:
        return existing_order
    

    total_amount = 0
    order_items = []

    for item in items_data:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {product.name}")

        price = product.price
        total_amount += price * item.quantity

        # reduce stock
        product.stock -= item.quantity

        order_items.append({
            "product_id": product.id,
            "quantity": item.quantity,
            "price": price
        })

    # create order
    order = Order(user_id=user_id, total_amount=total_amount, idempotency_key=idempotency_key)
    db.add(order)
    db.commit()
    db.refresh(order)

    # create order items
    for item in order_items:
        db_item = OrderItem(order_id=order.id, **item)
        db.add(db_item)

    db.commit()
    
    create_notification(db, user_id, "Order placed successfully")

    if background_tasks:
        background_tasks.add_task(process_order, order.id)

    return order


def get_order(db: Session, order_id: int, user_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # optional: restrict access
    if order.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return order


def get_user_orders(db: Session, user_id: int):
    return db.query(Order).filter(Order.user_id == user_id).all()


def update_order_status(db: Session, order_id: int, new_status: str):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    current_status = order.status

    # ❌ Prevent invalid transitions
    if new_status not in VALID_TRANSITIONS[current_status]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change from {current_status} to {new_status}"
        )

    order.status = new_status
    db.commit()
    db.refresh(order)


    create_notification(db, order.user_id, f"Order{new_status}")


    asyncio.create_task(
        manager.send_update(order_id, {
            "order_id": order_id,
            "status": new_status
        })
    )

    return order