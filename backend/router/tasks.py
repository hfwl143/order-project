...
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, crud, schemas
from database import get_db
from auth import get_current_user
router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/tasks",response_model=list[schemas.TaskOut])
def list_tasks(completed: bool | None = None, db: Session = Depends(get_db),user: models.User =Depends(get_current_user)):
    return crud.get_tasks(db,completed=completed,owner_id=user.id)

@router.get("/tasks/{task_id}",response_model= schemas.TaskOut)
def read_task(task_id: int,user: models.User =Depends(get_current_user),db: Session = Depends(get_db)):
    task = crud.get_task(db,task_id,user.id)
    if not task:
        raise HTTPException(status_code=404,detail="任务不存在")
    return task

@router.post("/tasks",response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate,user: models.User = Depends(get_current_user),db: Session = Depends(get_db)):
    return crud.create_task(db,task,user.id)

@router.put("/tasks/{task_id}",response_model= schemas.TaskOut)
def update_task(task_id: int,task: schemas.TaskUpdate,user: models.User =Depends(get_current_user),db: Session = Depends(get_db)):
    db_task = crud.get_task(db,task_id,user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return crud.update_task(db,db_task,task)

@router.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db),user: models.User =Depends(get_current_user)):
    db_task = crud.get_task(db, task_id,user.id)
    if not db_task:
        raise HTTPException(status_code=404, detail="任务不存在")
    crud.delete_task(db, db_task)

...