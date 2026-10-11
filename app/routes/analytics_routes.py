from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vendor import Vendor
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.transaction import Transaction
from app.schemas.transaction_schema import TransactionCreate, TransactionOut

router = APIRouter(tags=["Analytics & Transactions"])


# ---------- Transactions ----------
@router.post("/transactions/", response_model=TransactionOut, status_code=201)
def create_transaction(tx: TransactionCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.product_id == tx.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < tx.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    amount = round(product.price * tx.quantity, 2)

    product.stock -= tx.quantity
    inv = db.query(Inventory).filter(Inventory.product_id == product.product_id).first()
    if inv:
        inv.current_stock = product.stock

    record = Transaction(
        product_id=product.product_id,
        vendor_id=product.vendor_id,
        quantity=tx.quantity,
        amount=amount,
        transaction_date=tx.transaction_date or date.today(),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/transactions/", response_model=List[TransactionOut])
def list_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).order_by(Transaction.transaction_id).all()


# ---------- Analytics ----------
@router.get("/analytics/summary")
def summary(db: Session = Depends(get_db)):
    revenue, count, units = db.query(
        func.coalesce(func.sum(Transaction.amount), 0),
        func.count(Transaction.transaction_id),
        func.coalesce(func.sum(Transaction.quantity), 0),
    ).one()
    return {
        "total_revenue": round(float(revenue), 2),
        "total_transactions": count,
        "total_units_sold": int(units),
        "total_vendors": db.query(Vendor).count(),
        "total_products": db.query(Product).count(),
    }


@router.get("/analytics/revenue-by-vendor")
def revenue_by_vendor(db: Session = Depends(get_db)):
    rows = (
        db.query(Vendor.business_name,
                 func.sum(Transaction.amount).label("revenue"))
        .join(Transaction, Transaction.vendor_id == Vendor.vendor_id)
        .group_by(Vendor.business_name)
        .order_by(func.sum(Transaction.amount).desc())
        .all()
    )
    return [{"vendor": r[0], "revenue": round(float(r[1]), 2)} for r in rows]


@router.get("/analytics/top-products")
def top_products(limit: int = 10, db: Session = Depends(get_db)):
    rows = (
        db.query(Product.product_name,
                 func.sum(Transaction.quantity).label("units"),
                 func.sum(Transaction.amount).label("revenue"))
        .join(Transaction, Transaction.product_id == Product.product_id)
        .group_by(Product.product_name)
        .order_by(func.sum(Transaction.amount).desc())
        .limit(limit)
        .all()
    )
    return [{"product": r[0], "units": int(r[1]), "revenue": round(float(r[2]), 2)}
            for r in rows]


@router.get("/analytics/daily-revenue")
def daily_revenue(db: Session = Depends(get_db)):
    rows = (
        db.query(Transaction.transaction_date,
                 func.sum(Transaction.amount))
        .group_by(Transaction.transaction_date)
        .order_by(Transaction.transaction_date)
        .all()
    )
    return [{"date": str(r[0]), "revenue": round(float(r[1]), 2)} for r in rows]


@router.get("/analytics/consistency")
def consistency_check(db: Session = Depends(get_db)):
    total = float(db.query(func.coalesce(func.sum(Transaction.amount), 0)).scalar())
    by_vendor = sum(r["revenue"] for r in revenue_by_vendor(db))

    mismatched = (
        db.query(Transaction)
        .join(Product, Product.product_id == Transaction.product_id)
        .filter(Product.vendor_id != Transaction.vendor_id)
        .count()
    )
    n = db.query(Transaction).count()
    consistent = n - mismatched
    pct = 100.0 if n == 0 else round(consistent / n * 100, 2)
    return {
        "total_revenue": round(total, 2),
        "sum_of_vendor_revenue": round(by_vendor, 2),
        "totals_match": abs(total - by_vendor) < 0.01,
        "transactions_checked": n,
        "mismatched_transactions": mismatched,
        "consistency_percent": pct,
    }