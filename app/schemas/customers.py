from __future__ import annotations
from .common import OrmBase


class CustomerBase(OrmBase):
    name: str

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int