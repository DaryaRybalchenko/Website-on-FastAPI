from __future__ import annotations
from sqlalchemy import Column, Integer, String
from ..database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)  # название отдела