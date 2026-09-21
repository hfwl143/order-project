from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models, schemas, crud
from database import get_db
from auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/api")

@router.post("/register",response_model=schemas.Token)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db,user_in.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    if len(user_in.password) < 6:
        raise HTTPException(status_code=400, detail="密码至少 6 位")

    hashed_pwd = hash_password(user_in.password)
    new_user = crud.create_user(db,user_in.username,hashed_pwd)
    return {"access_token": create_token(new_user.id), "token_type": "bearer"}

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return {"access_token": create_token(user.id), "token_type": "bearer"}