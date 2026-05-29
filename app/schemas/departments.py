from __future__ import annotations
from .common import OrmBase


class DepartmentBase(OrmBase):
    name: str

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentUpdate(DepartmentBase):
    pass

class Department(DepartmentBase):
    id: int