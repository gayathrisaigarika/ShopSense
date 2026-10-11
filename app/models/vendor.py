from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base


class Vendor(Base):
    __tablename__ = "vendors"

    vendor_id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String(200), nullable=False)
    owner_name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20))
    category = Column(String(100))
    status = Column(String(20), default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)