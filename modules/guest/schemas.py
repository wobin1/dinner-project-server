from pydantic import BaseModel
from typing import Optional


class GuestModel(BaseModel):
    id: Optional[int] =None
    full_name: str
    email: str
    phone_number: str
    church: int
    attendance_status: Optional[bool] =None


class GetGuestModel(BaseModel):

    id: Optional[int]=None
    full_name: str
    email: str
    phone_number: str
    church: int
    attendance_status: Optional[bool] =None