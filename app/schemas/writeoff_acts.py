from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class WriteOffActBase(BaseModel):
    organization_id: int
    act_number: str
    act_date: date
    commission_chairman_id: int
    commission_member1_id: int
    commission_member2_id: Optional[int] = None
    commission_member3_id: Optional[int] = None
    created_by_id: int
    department_id: int
    # Убраны reason и basis

class WriteOffActCreate(WriteOffActBase):
    items: List['WriteOffActItemCreate'] = []

class WriteOffActUpdate(WriteOffActBase):
    items: List['WriteOffActItemCreate'] = []

class WriteOffActItemBase(BaseModel):
    product_id: int
    inventory_number: str
    commissioning_date: Optional[date] = None
    initial_cost: float
    useful_life: int
    actual_life: int
    residual_value: float
    item_reason: Optional[str] = None

class WriteOffActItemCreate(WriteOffActItemBase):
    pass