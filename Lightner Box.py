from dotenv import load_dotenv
import os

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import inspect

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables")
if not DATABASE_URL.startswith(("sqlite://", "postgresql://", "mysql://", "mariadb://")):
    raise ValueError(f" خطا: مقدار DATABASE_URL نامعتبر است: {DATABASE_URL}")
print(f" مقدار DATABASE_URL: {DATABASE_URL}")

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


engine = create_engine(DATABASE_URL)
print("اتصال به دیتابیس برقرار شد!")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
print("جدول پایگاه داده ایجاد شد!")

inspector = inspect(engine)
tables = inspector.get_table_names()
print(" جداول موجود در دیتابیس:", tables)

db_path = os.path.abspath("mydb.db")
print(f" مسیر واقعی دیتابیس: {db_path}")
