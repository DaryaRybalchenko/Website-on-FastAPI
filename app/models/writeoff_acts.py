from __future__ import annotations
from sqlalchemy import Column, Integer, ForeignKey, Date, String, Text, Numeric
from sqlalchemy.orm import relationship
from ..database import Base 

class WriteOffAct(Base):
    __tablename__ = "writeoff_acts"

    id = Column(Integer, primary_key=True, index=True)
    
    # Основные поля акта списания
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    act_number = Column(String(50), nullable=False)
    act_date = Column(Date, nullable=False)
    
    # Комиссия
    commission_chairman_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    commission_member1_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    commission_member2_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    commission_member3_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    
    # Служебные поля
    created_by_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    
    # Связи
    organization = relationship("Organization")
    commission_chairman = relationship("Employee", foreign_keys=[commission_chairman_id])
    commission_member1 = relationship("Employee", foreign_keys=[commission_member1_id])
    commission_member2 = relationship("Employee", foreign_keys=[commission_member2_id])
    commission_member3 = relationship("Employee", foreign_keys=[commission_member3_id])
    created_by = relationship("Employee", foreign_keys=[created_by_id])
    department = relationship("Department")
    
    # Позиции акта
    items = relationship(
        "WriteOffActItem",
        back_populates="writeoff_act",
        cascade="all, delete-orphan",
    )


class WriteOffActItem(Base): 
    __tablename__ = "writeoff_act_items"

    id = Column(Integer, primary_key=True, index=True)
    writeoff_act_id = Column(Integer, ForeignKey("writeoff_acts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # Характеристики основного средства
    inventory_number = Column(String(100), nullable=False)
    commissioning_date = Column(Date, nullable=False)  # Дата ввода в эксплуатацию
    initial_cost = Column(Numeric(12, 2), nullable=False)  # Первоначальная стоимость
    useful_life = Column(Integer, nullable=False)  # Срок полезного использования (месяцев)
    actual_life = Column(Integer, nullable=False)  # Фактический срок эксплуатации (месяцев)
    residual_value = Column(Numeric(12, 2), nullable=False)  # Остаточная стоимость
    
    # Причина списания для конкретного объекта
    item_reason = Column(Text, nullable=True)
    
    # Связи
    writeoff_act = relationship("WriteOffAct", back_populates="items")
    product = relationship("Product")