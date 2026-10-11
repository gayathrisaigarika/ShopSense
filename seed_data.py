import random
from datetime import date, timedelta

from app.database import SessionLocal, Base, engine
from app.models.vendor import Vendor
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.transaction import Transaction

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if db.query(Vendor).count() > 0:
    print("Data already exists, skipping.")
    raise SystemExit

vendors_data = [
    ("TechNova", "Arun Kumar", "technova@example.com", "9876543210", "Electronics"),
    ("StyleHub", "Priya Rao", "stylehub@example.com", "9876501234", "Fashion"),
    ("HomeEase", "Ravi Teja", "homeease@example.com", "9876505678", "Home"),
    ("FreshBasket", "Sana Khan", "freshbasket@example.com", "9876509999", "Grocery"),
]
vendors = []
for b, o, e, p, c in vendors_data:
    v = Vendor(business_name=b, owner_name=o, email=e, phone=p,
               category=c, status="Approved")
    db.add(v)
    vendors.append(v)
db.flush()

catalog = {
    "Electronics": [("Wireless Earbuds", 1999), ("Smart Watch", 3499), ("Power Bank", 1299)],
    "Fashion": [("Denim Jacket", 2499), ("Sneakers", 2999), ("Cotton T-Shirt", 599)],
    "Home": [("Table Lamp", 899), ("Cookware Set", 2799), ("Wall Clock", 699)],
    "Grocery": [("Organic Rice 5kg", 450), ("Olive Oil 1L", 799), ("Green Tea Box", 299)],
}
products = []
for v in vendors:
    for name, price in catalog[v.category]:
        p = Product(product_name=name, category=v.category, price=price,
                    stock=500, vendor_id=v.vendor_id)
        db.add(p)
        products.append(p)
db.flush()

for p in products:
    db.add(Inventory(product_id=p.product_id, current_stock=p.stock,
                     warehouse="Hyderabad WH", reorder_level=50))

for _ in range(200):
    p = random.choice(products)
    qty = random.randint(1, 5)
    p.stock -= qty
    db.add(Transaction(
        product_id=p.product_id, vendor_id=p.vendor_id, quantity=qty,
        amount=round(p.price * qty, 2),
        transaction_date=date.today() - timedelta(days=random.randint(0, 30)),
    ))
db.flush()

for inv in db.query(Inventory).all():
    inv.current_stock = db.get(Product, inv.product_id).stock

db.commit()
print("Sample data inserted")