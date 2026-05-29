# app/schemas/units.py
from __future__ import annotations
from .common import OrmBase

class UnitBase(OrmBase):
    name: str

class UnitCreate(UnitBase):
    pass

class UnitUpdate(UnitBase):
    pass

class Unit(UnitBase):
    id: int