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


