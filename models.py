
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, UTC

Base = declarative_base()


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
