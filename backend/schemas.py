from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime
from enum import Enum

class OrderTag(str, Enum):
    编程 = "编程"
    PS设计 = "PS设计"
    绘图 = "绘图"
    文案 = "文案"

class OrderCreate(BaseModel):
    title: str
    description: str
    tag: OrderTag
    deadline: str | None = None

class ProfileUpdate(BaseModel):
    wechat: str | None = None
    phone: str | None = None


class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):

    """Token模型类，用于表示认证令牌信息
    
    继承自BaseModel，通常用于API响应中的令牌表示
    """
    access_token: str  # 访问令牌，字符串类型，用于身份验证
    token_type: str = "bearer"  # 令牌类型，字符串类型，默认值为"bearer"



