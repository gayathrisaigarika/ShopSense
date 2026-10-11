from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(200), nullable=False)
    category = Column(String(100))
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    vendor_id = Column(Integer, ForeignKey("vendors.vendor_id"), nullable=False)