from sqlalchemy import (
    Column, Integer, String, Date, Boolean, DateTime,
    Enum, CheckConstraint, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.db import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    roll_no = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False, index=True)
    gender = Column(Enum("male", "female", "other", name="gender_enum"))
    age = Column(Integer)
    fees = Column(Integer, server_default="0")
    admission_date = Column(DateTime, server_default=func.now())

    __table_args__ = (
        CheckConstraint('age >= 1 AND age <= 120', name="check_age"),
        UniqueConstraint('roll_no', name='unique_rollno'),
        Index('idx_name_age', 'name', 'age'),
    )
