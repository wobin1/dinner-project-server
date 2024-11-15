from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    full_name: str
    email: str
    password: str
    phone_number: str
    is_church: Optional[bool]=None
    is_bouncer: Optional[bool]=None
    is_admin: Optional[bool]=None


class GetUsersModel(BaseModel):

    id: Optional[int]=None
    full_name: str
    email: str
    password: str
    phone_number: str
    is_active: bool
    is_church: bool
    is_admin: bool