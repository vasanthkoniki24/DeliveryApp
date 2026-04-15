from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.product import Product


def create_product(db: Session, data):
    product = Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(db: Session):
    return db.query(Product).all()


def update_product(db: Session, product_id: int, data):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product