from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.order import Order
from app.models.order import OrderItem
from app.models.product import Product


# ✅ 1. Orders Summary
def get_orders_summary(db: Session):
    total_orders = db.query(func.count(Order.id)).scalar()

    status_counts = db.query(
        Order.status,
        func.count(Order.id)
    ).group_by(Order.status).all()

    return {
        "total_orders": total_orders,
        "status_counts": dict(status_counts)
    }


# ✅ 2. Total Revenue
def get_total_revenue(db: Session):
    total_revenue = db.query(func.sum(Order.total_amount)).scalar()

    return {
        "total_revenue": total_revenue or 0
    }


# ✅ 3. Top Products
def get_top_products(db: Session):
    results = db.query(
        Product.name,
        func.sum(OrderItem.quantity).label("total_sold")
    ).join(OrderItem, Product.id == OrderItem.product_id)\
     .group_by(Product.name)\
     .order_by(func.sum(OrderItem.quantity).desc())\
     .limit(5)\
     .all()

    return [
        {"product_name": name, "total_sold": total}
        for name, total in results
    ]