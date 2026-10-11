from app.database import Base, engine

from app.models.vendor import Vendor
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.transaction import Transaction

Base.metadata.create_all(bind=engine)

print("Tables Created")