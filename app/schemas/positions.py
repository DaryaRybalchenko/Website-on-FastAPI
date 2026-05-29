from __future__ import annotations
from .common import OrmBase


class PositionBase(OrmBase):
    name: str

class PositionCreate(PositionBase):
    pass

class PositionUpdate(PositionBase):
    pass

class Position(PositionBase):
    id: int