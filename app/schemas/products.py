from __future__ import annotations
from .common import OrmBase


class ProductBase(OrmBase):
    name: str
    price: float
    unit_id: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int