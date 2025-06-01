
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

# از Base در فایل database.py استفاده می کنیم.
from .database import Base

from sqlalchemy.orm import relationship
from datetime import datetime, UTC


class MainBox(Base):
    __tablename__ = "LightnerBox"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    StepName = Column(String, index=True)


class FlashCard(Base):
    __tablename__ = "LightnerBoxCard"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    question = Column(String, index=True)
    answer = Column(String, index=True)
    step = Column(String, index=True)
    StepStartDate = Column(String, index=True)
    ShowDateOfCard = Column(String, index=True)
    LightnerBoxId = Column(Integer, ForeignKey('LightnerBox.id'))


class User(Base):
    __tablename__ = "LightnerUsers"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    cards = relationship("card", back_populates="user")


class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('LightnerUsers.id'), nullable=False)
    question = Column(String, index=True, nullable=False)
    answer = Column(String, index=True, nullable=False)
    category = Column(String, nullable=True)
    # مرحله جعبه لایتنر
    box = Column(Integer, default=1)
    # تاریخ نمایش بعدی
    next_due_date = Column(DateTime, default=lambda: datetime.now(UTC))
    user = relationship("User", back_populates="cards")
