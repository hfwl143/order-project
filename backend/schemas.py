from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):

    """Token模型类，用于表示认证令牌信息
    
    继承自BaseModel，通常用于API响应中的令牌表示
    """
    access_token: str  # 访问令牌，字符串类型，用于身份验证
    token_type: str = "bearer"  # 令牌类型，字符串类型，默认值为"bearer"



# 创建任务时的请求体
class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = ""
    due_date: Optional[date] = None


# 更新任务时的请求体（所有字段可选）
class TaskUpdate(BaseModel):

    # 任务更新模型类，继承自BaseModel
    # 用于更新任务信息的请求体数据模型
    title: Optional[str] = Field(None, min_length=1, max_length=100)  # 任务标题，可选字段，长度限制在1-100个字符之间
    description: Optional[str] = None  # 任务描述，可选字段，无长度限制
    completed: Optional[bool] = None  # 任务完成状态，可选字段，布尔值
    due_date: Optional[date] = None  # 任务截止日期，可选字段，日期类型


# 返回给前端的任务格式
class TaskOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
    due_date: Optional[date] = None

    class Config:

        # 这是一个配置类，用于设置某些全局或特定功能的配置选项
        from_attributes = True  # 允许从 ORM 对象直接转换，启用此选项后，可以将 ORM 对象直接转换为字典或其他数据结构