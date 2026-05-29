from __future__ import annotations
from .common import OrmBase


class AccountBase(OrmBase):
    account: str
    bank_name: str
    bank_identity_number: str

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    pass

class Account(AccountBase):
    id: int