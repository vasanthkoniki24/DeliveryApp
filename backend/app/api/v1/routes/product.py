from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.services.product_service import create_product, get_products, update_product
from app.dependencies.auth import get_db, require_role

router = APIRouter(prefix="/products", tags=["Products"])


# ✅ Create Product (Admin only)
@router.post("/", response_model=ProductResponse)
def add_product(
    data: ProductCreate,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):
    return create_product(db, data)


# ✅ Get All Products (Public)
@router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return get_products(db)


# ✅ Update Product (Admin only)
@router.patch("/{product_id}", response_model=ProductResponse)
def edit_product(
    product_id: int,
    data: ProductUpdate,
    db: Session = Depends(get_db),
    user = Depends(require_role("admin"))
):
    return update_product(db, product_id, data)