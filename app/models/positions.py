from __future__ import annotations
from sqlalchemy import Column, Integer, String
from ..database import Base


class Position(Base):
    __tablename__ = "positions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)  # название должности