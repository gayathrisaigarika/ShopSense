from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vendor import Vendor
from app.models.product import Product
from app.models.inventory import Inventory
from app.schemas.product_schema import ProductCreate, ProductOut

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductOut, status_code=201)
def add_product(data: ProductCreate, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.vendor_id == data.vendor_id).first()
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    product = Product(
        product_name=data.product_name,
        category=data.category,
        price=data.price,
        stock=data.stock,
        vendor_id=data.vendor_id,
    )
    db.add(product)
    db.flush()

    db.add(Inventory(
        product_id=product.product_id,
        current_stock=data.stock,
        warehouse=data.warehouse,
        reorder_level=data.reorder_level,
    ))
    db.commit()
    db.refresh(product)
    return product


@router.get("/", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).order_by(Product.product_id).all()