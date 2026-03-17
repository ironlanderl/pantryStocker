from typing import Annotated
from datetime import date, datetime # Import datetime for parsing

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from sqlalchemy import event
from sqlalchemy.engine import Engine

from backend.sql_models import Profile, Product, Location, InventoryItem


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args, echo=True, pool_pre_ping=True)

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


app = FastAPI()

# TODO: Make this more granular
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# ---- BEGIN LOCATIONS ----
@app.post("/locations/", response_model=Location)
def create_location(location: Location, session: SessionDep) -> Location:
    session.add(location)
    session.commit()
    session.refresh(location)
    return location

@app.get("/locations/", response_model=list[Location])
def read_locations(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Location]:
    locations = session.exec(select(Location).offset(offset).limit(limit)).all()
    return locations

@app.get("/locations/{location_id}")
def read_location(location_id: int, session: SessionDep) -> Location:
    location = session.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="location not found")
    return location

@app.delete("/locations/{location_id}")
def delete_location(location_id: int, session: SessionDep):
    location = session.get(Location, location_id)
    if not location:
        raise HTTPException(status_code=404, detail="location not found")
    session.delete(location)
    session.commit()
    return {"ok": True}

# ---- END LOCATION ----
# ---- BEGIN PRODUCT ----
@app.post("/products/", response_model=Product)
def create_product(product: Product, session: SessionDep) -> Product:
    session.add(product)
    session.commit()
    session.refresh(product)
    return product

@app.get("/products/", response_model=list[Product])
def read_products(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[Product]:
    products = session.exec(select(Product).offset(offset).limit(limit)).all()
    return products

@app.get("/products/{product_id}")
def read_product(product_id: str, session: SessionDep) -> Product:
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    return product

@app.delete("/products/{product_id}")
def delete_product(product_id: str, session: SessionDep):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="product not found")
    session.delete(product)
    session.commit()
    return {"ok": True}
# ---- END PRODUCT ----
# ---- BEGIN INVENTORY_ITEM ----
@app.post("/inventory_items/", response_model=InventoryItem)
def create_inventory_item(inventory_item: InventoryItem, session: SessionDep) -> InventoryItem:
    # Manually convert expiration_date from string to date object if it's a string
    if isinstance(inventory_item.expiration_date, str):
        try:
            inventory_item.expiration_date = datetime.strptime(inventory_item.expiration_date, '%Y-%m-%d').date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format for expiration_date. Expected YYYY-MM-DD.")
    session.add(inventory_item)
    session.commit()
    session.refresh(inventory_item)
    return inventory_item


@app.get("/inventory_items/", response_model=list[InventoryItem])
def read_inventory_items(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[InventoryItem]:
    inventory_items = session.exec(select(InventoryItem).offset(offset).limit(limit)).all()
    return inventory_items


@app.get("/inventory_items/{inventory_item_id}", response_model=InventoryItem)
def read_inventory_item(inventory_item_id: int, session: SessionDep) -> InventoryItem:
    inventory_item = session.get(InventoryItem, inventory_item_id)
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    return inventory_item

@app.get("/inventory_items/by_product/{product_id}", response_model=list[InventoryItem])
def read_inventory_by_product(product_id: str, session: SessionDep) -> list[InventoryItem]:
    inventory_items = session.exec(select(InventoryItem).where(InventoryItem.product_id == product_id)).all()
    return inventory_items

@app.delete("/inventory_items/{inventory_item_id}")
def delete_inventory_item(inventory_item_id: int, session: SessionDep):
    inventory_item = session.get(InventoryItem, inventory_item_id)
    if not inventory_item:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    session.delete(inventory_item)
    session.commit()
    return {"ok": True}
# ---- END INVENTORY_ITEM ----
