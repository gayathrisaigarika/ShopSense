from fastapi import FastAPI

from app.database import Base, engine
from app.models import vendor, product, inventory, transaction  # noqa: F401
from app.routes import vendor_routes, product_routes, analytics_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ShopSense - Marketplace Foundation")

app.include_router(vendor_routes.router)
app.include_router(product_routes.router)
app.include_router(analytics_routes.router)


@app.get("/")
def root():
    return {"message": "ShopSense API is running"}