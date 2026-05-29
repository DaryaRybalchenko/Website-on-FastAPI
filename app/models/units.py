from __future__ import annotations
from sqlalchemy import Column, Integer, String
from ..database import Base


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)  # напр. "шт", "кг", "л"