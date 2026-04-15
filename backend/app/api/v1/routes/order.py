from fastapi import APIRouter, Depends, Header, BackgroundTasks
from sqlalchemy.orm import Session

from app.schemas.order import OrderCreate, OrderResponse
from app.services.order_service import create_order, get_order, get_user_orders, update_order_status
from app.dependencies.auth import get_db, get_current_user, require_role

from app.models.order import Order

router = APIRouter(prefix="/orders", tags=["Orders"])


# ✅ Create Order
@router.post("/", response_model=OrderResponse)
def place_order(
    data: OrderCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user = Depends(get_current_user),
    idempotency_key: str = Header(default=None)
):
    return create_order(db, user.id, data.items, idempotency_key, background_tasks)


# ✅ Get Single Order
@router.get("/{order_id}", response_model=OrderResponse)
def fetch_order(
    order_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return get_order(db, order_id, user.id)


# ✅ Get All Orders (User)
@router.get("/", response_model=list[OrderResponse])
def fetch_orders(
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return get_user_orders(db, user.id)



@router.patch("/{order_id}/status", response_model=OrderResponse)
def change_status(
    order_id: int,
    new_status: str,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))  # ✅ ONLY ADMIN
):
    return update_order_status(db, order_id, new_status)


@router.get("/admin/all", response_model=list[OrderResponse])
def get_all_orders(db: Session = Depends(get_db), user = Depends(require_role("admin"))):
    return db.query(Order).all()
