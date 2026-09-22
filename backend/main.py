from fastapi import FastAPI, Depends, HTTPException,APIRouter
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from database import engine, Base, SessionLocal, get_db
import models
import crud
import schemas
from auth import create_token,get_current_user
from router.auth import router as auth_router
# 生命周期管理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # ========= yield【之前】：程序启动前执行（原来的 startup） =========
    print("应用启动，开始检查/创建数据库表")
    Base.metadata.create_all(bind=engine)

    yield   # ✅ 这里是分界线！程序走到这里，才正式开始接收接口请求

    # ========= yield【之后】：服务关闭时执行（原来的 shutdown） =========
    print("应用正在关闭，释放资源")
    # 这里可以写关闭数据库连接等清理逻辑

app = FastAPI(lifespan=lifespan)

# 允许前端 localhost:5173 跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"] ,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/")
def read_root():
    return {"message": "Hello from backend"}

@router.get("/health")
def health():
    return {"status": "ok"}



app.include_router(auth_router)

app.include_router(router)