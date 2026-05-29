from __future__ import annotations
from sqlalchemy import Column, Integer, String
from ..database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account = Column(String(100), nullable=False)           # номер расчётного счёта
    bank_name = Column(String(200), nullable=False)         # наименование банка
    bank_identity_number = Column(String(50), nullable=False)  # БИК