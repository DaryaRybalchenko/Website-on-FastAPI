from __future__ import annotations
from datetime import date
from typing import List
from .common import OrmBase


class ProxyItemBase(OrmBase):
    product_id: int
    amount: int

class ProxyItemCreate(ProxyItemBase):
    pass

class ProxyItem(ProxyItemBase):
    id: int

class ProxyBase(OrmBase):
    organization_id: int
    employee_id: int
    customer_id: int
    date_of_issue: date
    is_valid_until: date

class ProxyCreate(ProxyBase):
    items: List[ProxyItemCreate] = []

class ProxyUpdate(ProxyBase):
    items: List[ProxyItemCreate] = []

class Proxy(ProxyBase):
    id: int
    items: List[ProxyItem] = []