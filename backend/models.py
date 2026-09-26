from sqlalchemy.sql import func
from sqlalchemy import Column, DateTime,Integer, String, Text, Boolean, DateTime, Date, Float, Numeric,ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    username = Column(String(50),unique=True,nullable=False)
    hashed_password = Column(String(200),nullable=False)
    wechat = Column(String(100))
    phone = Column(String(20))


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    tag = Column(String(20), nullable=False)              # 编程/PS设计/绘图/文案
    deadline = Column(String(20))                          # 如 "2026-09-30 18:00"
    order_status = Column(String(20), default="未接单")     # 未接单/已接单/已关闭
    abandon_requested = Column(Boolean, default=False)
    abandon_request_time = Column(DateTime)
    publisher_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    taker_id = Column(Integer, ForeignKey("users.id"))
    create_time = Column(DateTime, default=datetime.utcnow)
    update_time = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    publisher = relationship("User", foreign_keys=[publisher_id])
    taker = relationship("User", foreign_keys=[taker_id])


