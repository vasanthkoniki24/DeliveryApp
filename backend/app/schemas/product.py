from pydantic import BaseModel, Field

# create product
class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    image: str | None = None

# update product
class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
    image: str | None = None

# response product
class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None
    price: float
    stock: int

    image: str | None 

    class Config:
        from_attributes = True