import datetime
from pydantic import BaseModel


class WTAEventBase(BaseModel):
    date: datetime.datetime


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


class UserInDb(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
