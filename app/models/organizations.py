from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)       # название организации
    address = Column(String(255), nullable=False)    # адрес
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)  # внешний ключ на счёт
    chief = Column(String(100), nullable=False)      # руководитель
    financial_chief = Column(String(100), nullable=False)  # главный бухгалтер

    account = relationship("Account")