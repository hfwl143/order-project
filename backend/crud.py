from sqlalchemy.orm import Session
import models
from datetime import datetime, timedelta
from schemas import OrderCreate

ABANDON_TIMEOUT = timedelta(days=3)


def get_tasks_by_owner(db: Session, owner_id: int):
   return db.query(models.Task).filter(models.Task.owner_id == owner_id)

def get_user_by_username(db: Session,username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, username: str, hashed_password: str):
    db_user=models.User(username = username,hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user





def order_to_dict(db: Session, order: models.Order, user_id: int) -> dict:
    """统一出口：超时兜底 + 联系方式权限 + 计算字段"""
    # ⏰ 放弃申请超3天 → 自动同意
    if (order.abandon_requested and order.order_status == "已接单"
            and order.abandon_request_time
            and datetime.utcnow() - order.abandon_request_time > ABANDON_TIMEOUT):
        order.order_status = "未接单"
        order.taker_id = None
        order.abandon_requested = False
        order.abandon_request_time = None
        db.commit()
        db.refresh(order)

    contact = None
    if order.order_status == "已接单" and user_id in (order.publisher_id, order.taker_id):
        other = order.taker if user_id == order.publisher_id else order.publisher
        contact = {"wechat": other.wechat, "phone": other.phone}

    return {
        "id": order.id, "title": order.title,
        "description": order.description, "tag": order.tag,
        "deadline": order.deadline, "order_status": order.order_status,
        "abandon_requested": order.abandon_requested,
        "publisher_id": order.publisher_id, "taker_id": order.taker_id,
        "create_time": str(order.create_time),
        "is_mine": user_id in (order.publisher_id, order.taker_id),
        "my_role": "publisher" if user_id == order.publisher_id
                   else ("taker" if user_id == order.taker_id else None),
        "contact": contact,
    }


def create_order(db: Session, user_id: int, data: OrderCreate) -> models.Order:
    order = models.Order(**data.dict(), publisher_id=user_id)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_hall_orders(db: Session, tag: str | None = None) -> list[models.Order]:
    """任务大厅：只展示未接单"""
    q = db.query(models.Order).filter(models.Order.order_status == "未接单")
    if tag:
        q = q.filter(models.Order.tag == tag)
    return q.order_by(models.Order.create_time.desc()).all()


def get_my_orders(db: Session, user_id: int, role: str) -> list[models.Order]:
    if role == "published":
        q = db.query(models.Order).filter(models.Order.publisher_id == user_id)
    else:
        q = db.query(models.Order).filter(models.Order.taker_id == user_id)
    return q.order_by(models.Order.abandon_requested.desc(),
                      models.Order.update_time.desc()).all()


def get_order(db: Session, order_id: int) -> models.Order | None:
    return db.query(models.Order).get(order_id)


def take_order(db: Session, order: models.Order, user_id: int) -> None:
    order.taker_id = user_id
    order.order_status = "已接单"
    db.commit()


def edit_order(db: Session, order: models.Order, data: OrderCreate) -> None:
    for k, v in data.dict().items():
        setattr(order, k, v)
    db.commit()


def request_abandon(db: Session, order: models.Order) -> None:
    order.abandon_requested = True
    order.abandon_request_time = datetime.utcnow()
    db.commit()


def handle_abandon(db: Session, order: models.Order, agree: bool) -> None:
    if agree:
        order.order_status = "未接单"
        order.taker_id = None
    order.abandon_requested = False
    order.abandon_request_time = None
    db.commit()


def close_order(db: Session, order: models.Order) -> None:
    order.order_status = "已关闭"
    db.commit()
