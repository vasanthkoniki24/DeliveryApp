import asyncio
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.order import Order
from app.services.ws_manager import manager 

# from app.services.order_worker import process_order 
from app.services.notification_service import create_notification

STATUS_FLOW = ["confirmed", "processing", "shipped", "delivered"]


async def process_order(order_id: int):
    db: Session = SessionLocal()

    try:
        order = db.query(Order).filter(Order.id == order_id).first()

        for status in STATUS_FLOW:
            await asyncio.sleep(3)  # simulate delay

            order.status = status
            db.commit()
            db.refresh(order)

            create_notification(db, order.user_id, f"Order{status}")

            # send real-time update
            await manager.send_update(order_id, {
                "order_id": order_id,
                "status": status
            })

    finally:
        db.close()