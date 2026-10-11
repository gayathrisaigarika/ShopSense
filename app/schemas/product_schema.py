from typing import Optional
from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    product_name: str = Field(..., min_length=2, max_length=200)
    category: Optional[str] = "General"
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    vendor_id: int
    warehouse: Optional[str] = "Main Warehouse"
    reorder_level: int = Field(default=10, ge=0)


class ProductOut(BaseModel):
    product_id: int
    product_name: str
    category: Optional[str]
    price: float
    stock: int
    vendor_id: int

    model_config = {"from_attributes": True}