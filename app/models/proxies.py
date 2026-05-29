from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from ..database import Base


class Proxy(Base):
    __tablename__ = "proxies"

    id = Column(Integer, primary_key=True, index=True)

    # FK: организация, сотрудник, контрагент
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    date_of_issue = Column(Date, nullable=False)     # дата выдачи
    is_valid_until = Column(Date, nullable=False)    # действительна до

    # связи для удобного отображения в шаблонах
    organization = relationship("Organization")
    employee = relationship("Employee")
    customer = relationship("Customer")

    # вложенные позиции доверенности
    items = relationship(
        "ProxyItem",
        back_populates="proxy",
        cascade="all, delete-orphan",
    )


class ProxyItem(Base):
    __tablename__ = "proxy_items"

    id = Column(Integer, primary_key=True, index=True)
    proxy_id = Column(Integer, ForeignKey("proxies.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    amount = Column(Integer, nullable=False)

    proxy = relationship("Proxy", back_populates="items")
    product = relationship("Product")   # для отображения имени и единицы