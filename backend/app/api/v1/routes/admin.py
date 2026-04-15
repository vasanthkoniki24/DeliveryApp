from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.services.admin_service import (
    get_orders_summary,
    get_total_revenue,
    get_top_products
)
from app.dependencies.auth import get_db, require_role



router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/admin-test")
def admin_test(user = Depends(require_role("admin"))):
    return {"msg": "Admin access"}


@router.get("/orders/summary")
def orders_summary(
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):
    return get_orders_summary(db) 


@router.get("/revenue")
def revenue(
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):
    return get_total_revenue(db) 


@router.get("/top-products")
def top_products(
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):
    return get_top_products(db)

