from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from ..deps import get_db, get_current_user
from ..models import Task, TaskStatus, TaskPriority, User
from ..schemas import TaskCreate, TaskUpdate, TaskOut

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskOut)
def create_task (payload: TaskCreate,
                 db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_user)):
    task = Task(
        user_id=current_user.id,
        title=payload.title,
        description=payload.description or "",
        status=TaskStatus(payload.status) if payload.status else TaskStatus.todo,
        priority=TaskPriority(payload.priority) if payload.priority else TaskPriority.medium,
        due_date=payload.due_date,
        assignee=payload.assignee,
        labels=payload.labels or "",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("", response_model=List[TaskOut])
def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    status: Optional[TaskStatus] = Query(None),
    priority: Optional[TaskPriority] = Query(None),
    q: Optional[str] = Query(None, description="タイトル/説明の部分一致検索"),
):
    query = db.query(Task).filter(Task.user_id == current_user.id)
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if q:
        like = f"%{q}%"
        query = query.filter((Task.title.ilike(like)) | (Task.description.ilike(like)))
    return query.order_by(Task.created_at.desc()).all()


@router.get("/{task_id}", response_model=TaskOut)
def get_task(task_id: int,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.patch("/{task_id}", response_model=TaskOut)
def update_task(task_id: int,
                payload: TaskUpdate,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    data = payload.dict(exclude_unset=True)
    if "status" in data and data["status"] is not None:
        data["status"] = TaskStatus(data["status"])
    if "priority" in data and data["priority"] is not None:
        data["priority"] = TaskPriority(data["priority"])
        
    for k, v in data.items():
        setattr(task, k, v)
    task.updated_at = datetime.utcnow()
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.user_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return None
