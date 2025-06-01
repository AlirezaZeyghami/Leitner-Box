
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    username: str


class Config:
    orm_mode = True


class CardBase(BaseModel):
    question: str
    answer: str
    category: Optional[str] = None


class CardCreate(CardBase):
    pass


class CardUpdate(CardBase):
    box: Optional[int] = None
    next_due_date: Optional[datetime] = None


class Card(CardBase):
    id: int
    box: int
    next_due_date: datetime
    user_id: int

    class Config:
        orm_mode = True
