from pydantic import BaseModel
from typing import List, Literal
from datetime import datetime

OrderStatus = Literal[
    "created",
    "confirmed",
    "processing",
    "shipped",
    "delivered"
]
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    id: int
    total_amount: float
    status: str
    created_at: datetime 
    updated_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True