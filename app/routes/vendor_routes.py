from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vendor import Vendor
from app.schemas.vendor_schema import VendorCreate, VendorOut, VendorStatusUpdate

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.post("/", response_model=VendorOut, status_code=201)
def register_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    if db.query(Vendor).filter(Vendor.email == vendor.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    new_vendor = Vendor(**vendor.model_dump(), status="Pending")
    db.add(new_vendor)
    db.commit()
    db.refresh(new_vendor)
    return new_vendor


@router.get("/", response_model=List[VendorOut])
def list_vendors(db: Session = Depends(get_db)):
    return db.query(Vendor).order_by(Vendor.vendor_id).all()


@router.put("/{vendor_id}/status", response_model=VendorOut)
def update_vendor_status(vendor_id: int, body: VendorStatusUpdate,
                         db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    vendor.status = body.status
    db.commit()
    db.refresh(vendor)
    return vendor