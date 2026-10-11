from sqlalchemy import Column, Integer, String, ForeignKey
from app.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    inventory_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    current_stock = Column(Integer, default=0)
    warehouse = Column(String(100))
    reorder_level = Column(Integer, default=10)