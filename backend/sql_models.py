from typing import List, Optional

from datetime import date

from sqlmodel import Field, Relationship, SQLModel


class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    age: int


class Product(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True) # id is string in legacy model
    name: str
    description: str = Field(default="")

    inventory_items: List["InventoryItem"] = Relationship(back_populates="item")


class Location(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    inventory_items: List["InventoryItem"] = Relationship(back_populates="location")


class InventoryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: str = Field(foreign_key="product.id")
    location_id: int = Field(foreign_key="location.id")
    expiration_date: date | None = Field(default=None)

    item: Product = Relationship(back_populates="inventory_items")
    location: Location = Relationship(back_populates="inventory_items")
