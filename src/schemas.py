import datetime
from typing import Optional
from pydantic import BaseModel


class WTAEventBase(BaseModel):
    date: datetime.date
    time: datetime.time


class WTAEventCreate(WTAEventBase):
    pass


class WTAEvent(WTAEventBase):
    id: int | None
    user_id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = True
    wta_events: list[WTAEvent] = []

    class Config:
        from_attributes = True
