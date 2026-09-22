from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime,Integer, String, Text, Boolean, DateTime, Date, Float, Numeric,ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    username = Column(String(50),unique=True,nullable=False)
    hashed_password = Column(String(200),nullable=False)
    tasks = relationship("Task",back_populates="owner")


