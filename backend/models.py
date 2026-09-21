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



class Task(Base):


    """
    Task类，表示一个任务实体，继承自Base类。
    定义了任务在数据库中的表结构及相关字段。
    """
    __tablename__ = "tasks"  # 指定数据库表名为"tasks"
    
    id = Column(Integer, primary_key=True, index=True)  # 任务ID，主键，建立索引
    title = Column(String(100), nullable=False)  # 任务标题，最大长度100，不可为空
    description = Column(Text, nullable=True, default="")  # 任务描述，文本类型，可为空，默认为空字符串
    completed = Column(Boolean, default=False)  # 任务完成状态，布尔类型，默认为未完成
    created_at = Column(DateTime, default=func.now(), nullable=False)  # 创建时间，默认为当前时间，不可为空
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)  # 更新时间，默认为当前时间，更新时自动更新，不可为空
    due_date = Column(Date, nullable=True)  # 截止日期，日期类型，可为空
    owner_id = Column(Integer, ForeignKey("users.id")) #  任务所有者ID，外键关联到users表的id字段
    owner = relationship("User", back_populates="tasks") #  与User模型建立双向关系，back_populates表示反向引用