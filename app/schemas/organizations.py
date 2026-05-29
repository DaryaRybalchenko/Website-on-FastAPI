from __future__ import annotations
from typing import Optional
from .common import OrmBase


class OrganizationBase(OrmBase):
    name: str
    address: str
    account_id: Optional[int] = None
    chief: str
    financial_chief: str

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int