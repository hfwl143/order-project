from sqlalchemy import create_engine#引擎函数
from sqlalchemy.orm import sessionmaker, DeclarativeBase# 导入SQLAlchemy ORM相关的sessionmaker和DeclarativeBase类
from config import settings

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL,pool_pre_ping=True) #  创建数据库引擎，并启用pool_pre_ping选项用于自动检测断开连接
SessionLocal = sessionmaker(bind=engine,autoflush=False) #  创建会话工厂，绑定到数据库引擎，并禁用自动刷新功能

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal() #  创建一个数据库会话
    try:
        yield db #  使用 yield 返回会话，允许其他代码使用这个数据库连接
    finally:
        db.close() #  确保在完成后关闭数据库会话，释放资源