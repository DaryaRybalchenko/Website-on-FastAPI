from __future__ import annotations
from datetime import date
from typing import Optional
from .common import OrmBase


class EmployeeBase(OrmBase):
    last_name: str
    first_name: str
    middle_name: Optional[str] = None
    post_id: int  # теперь id позиции, а не строка
    passport_series: str
    passport_number: str
    passport_issued_by: str
    passport_date_of_issue: date  # Pydantic спокойно примет "YYYY-MM-DD" строкой

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    id: int