from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr, Field


class ContactModel(BaseModel):
    first_name: str = Field('First_name', min_length=3, max_length=16)
    last_name: str = Field('Last_name', min_length=3, max_length=16)
    email: EmailStr
    phone: str = Field('00000000000',  max_length=16)
    birthday: date
    description: Optional[str]


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str = 'First_name'
    last_name: str = 'Last_name'
    email: EmailStr
    phone: str = '00000000000'
    birthday: date
    description: Optional[str]

    class Config:
        orm_mode = True
