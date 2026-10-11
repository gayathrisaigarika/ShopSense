from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class VendorCreate(BaseModel):
    business_name: str = Field(..., min_length=2, max_length=200)
    owner_name: Optional[str] = Field(default="N/A", max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(default=None, pattern=r"^\+?[0-9\- ]{7,15}$")
    category: Optional[str] = "General"


class VendorStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(Pending|Approved|Rejected)$")


class VendorOut(BaseModel):
    vendor_id: int
    business_name: str
    owner_name: Optional[str]
    email: str
    phone: Optional[str]
    category: Optional[str]
    status: str
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}