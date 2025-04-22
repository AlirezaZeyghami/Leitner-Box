
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables")
if not DATABASE_URL.startswith(("sqlite://", "postgresql://", "mysql://", "mariadb://")):
    raise ValueError(f" خطا: مقدار DATABASE_URL نامعتبر است: {DATABASE_URL}")
print(f" مقدار DATABASE_URL: {DATABASE_URL}")

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


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
