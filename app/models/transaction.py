from sqlalchemy import Column, Integer, Float, Date, ForeignKey
from app.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.vendor_id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(Date, nullable=False)
    