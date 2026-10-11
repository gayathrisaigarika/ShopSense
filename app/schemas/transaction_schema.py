from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class TransactionCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    transaction_date: Optional[date] = None


class TransactionOut(BaseModel):
    transaction_id: int
    product_id: int
    vendor_id: int
    quantity: int
    amount: float
    transaction_date: date

    model_config = {"from_attributes": True}