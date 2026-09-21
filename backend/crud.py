from sqlalchemy.orm import Session
import models
import schemas

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


def get_tasks(db: Session, completed: bool | None = None, owner_id: int | None = None):
    # 只有当 owner_id 不为空时，才去调用按用户查找的逻辑
    if owner_id is not None:
        query = get_tasks_by_owner(db, owner_id)
    else:
        query = db.query(models.Task) # 否则查询所有任务
        
    if completed is not None:
        query = query.filter(models.Task.completed == completed)
        
    return query.order_by(models.Task.created_at.desc()).all()


def get_task(db: Session,task_id: int,owner_id: int | None = None):
    if owner_id is not None:
        query = get_tasks_by_owner(db, owner_id)
    else:
        query = db.query(models.Task) # 否则查询所有任务
    return query.filter(models.Task.id == task_id).first()

def create_task(db: Session,task: schemas.TaskCreate,owner_id: int | None = None):
    db_task = models.Task(**task.model_dump(),owner_id = owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session,db_task: models.Task,task_update: schemas.TaskUpdate):
    for field, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task



def delete_task(db: Session,db_task: models.Task):
    db.delete(db_task)
    db.commit()