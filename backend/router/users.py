import re

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas
from database import get_db
from auth import get_current_user

router = APIRouter(prefix="/api/users", tags=["users"])

PHONE_RE = re.compile(r"^1[3-9]\d{9}$")
WECHAT_RE = re.compile(r"^[a-zA-Z][-_a-zA-Z0-9]{5,19}$")


@router.get("/me")
def get_my_profile(user: models.User = Depends(get_current_user)):
    """获取当前登录用户的联系方式资料"""
    return {"username": user.username, "wechat": user.wechat, "phone": user.phone}


@router.patch("/me")
def update_my_profile(
    payload: schemas.ProfileUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """更新当前登录用户的微信/手机号（省略的字段保持不变，空字符串表示清空）"""
    if payload.wechat is not None:
        wechat = payload.wechat.strip()
        if wechat and not WECHAT_RE.fullmatch(wechat):
            raise HTTPException(
                status_code=400,
                detail="微信号需以字母开头，为 6-20 位字母、数字、下划线或减号",
            )
        user.wechat = wechat or None

    if payload.phone is not None:
        phone = payload.phone.strip()
        if phone and not PHONE_RE.fullmatch(phone):
            raise HTTPException(status_code=400, detail="请输入正确的 11 位大陆手机号")
        user.phone = phone or None

    db.commit()
    db.refresh(user)
    return {"username": user.username, "wechat": user.wechat, "phone": user.phone}
