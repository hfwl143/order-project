from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
import crud
from auth import get_current_user
from database import get_db
router = APIRouter(prefix="/api/orders", tags=["订单"])


@router.post("")
def create_order(data: schemas.OrderCreate,
                 user: models.User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    order = crud.create_order(db, user.id, data)
    return crud.order_to_dict(db, order, user.id)


@router.get("")
def order_hall(tag: str | None = None,
               user: models.User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    orders = crud.get_hall_orders(db, tag)
    return [crud.order_to_dict(db, o, user.id) for o in orders]


@router.get("/mine")
def my_orders(role: str = "published",
              user: models.User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    if role not in ("published", "taken"):
        raise HTTPException(400, "role 参数只能是 published 或 taken")
    orders = crud.get_my_orders(db, user.id, role)
    return [crud.order_to_dict(db, o, user.id) for o in orders]


@router.post("/{order_id}/take")
def take_order(order_id: int,
               user: models.User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order or order.order_status != "未接单":
        raise HTTPException(400, "任务不存在或已被接单")
    if order.publisher_id == user.id:
        raise HTTPException(403, "不能接自己发布的任务")
    crud.take_order(db, order, user.id)
    return crud.order_to_dict(db, order, user.id)


@router.put("/{order_id}")
def edit_order(order_id: int, data: schemas.OrderCreate,
               user: models.User = Depends(get_current_user),
               db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order or order.publisher_id != user.id:
        raise HTTPException(403, "无权操作")
    if order.order_status != "未接单":
        raise HTTPException(400, "已接单任务不可编辑")
    crud.edit_order(db, order, data)
    return crud.order_to_dict(db, order, user.id)


@router.post("/{order_id}/abandon")
def request_abandon(order_id: int,
                    user: models.User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order or order.taker_id != user.id or order.order_status != "已接单":
        raise HTTPException(403, "无权操作")
    crud.request_abandon(db, order)
    return {"msg": "已提交申请，等待发单人处理（3天未处理将自动同意）"}


@router.post("/{order_id}/abandon/{decision}")
def handle_abandon(order_id: int, decision: str,
                   user: models.User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order or order.publisher_id != user.id or not order.abandon_requested:
        raise HTTPException(403, "无待处理的放弃申请")
    if decision not in ("agree", "reject"):
        raise HTTPException(400, "decision 只能是 agree 或 reject")
    crud.handle_abandon(db, order, agree=(decision == "agree"))
    return crud.order_to_dict(db, order, user.id)


@router.post("/{order_id}/close")
def close_order(order_id: int,
                user: models.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order or order.publisher_id != user.id:
        raise HTTPException(403, "无权操作")
    if order.order_status == "已接单":
        raise HTTPException(400, "已接单任务需先通过放弃流程解除")
    crud.close_order(db, order)
    return {"msg": "任务已关闭"}
