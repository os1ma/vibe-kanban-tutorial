from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime
from typing import List, Optional
from app import models, schemas


def get_todo(db: Session, todo_id: int):
    return db.query(models.Todo).filter(models.Todo.id == todo_id).first()


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()


def create_todo(db: Session, todo: schemas.TodoCreate):
    db_todo = models.Todo(**todo.dict())
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    db_todo = get_todo(db, todo_id)
    if db_todo:
        update_data = todo.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_todo, field, value)
        db_todo.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    db_todo = get_todo(db, todo_id)
    if db_todo:
        db.delete(db_todo)
        db.commit()
        return True
    return False


def filter_todos(
    db: Session,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    category: Optional[str] = None,
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(models.Todo)

    if status is not None:
        query = query.filter(models.Todo.status == status)

    if priority:
        query = query.filter(models.Todo.priority == priority)

    if category:
        query = query.filter(models.Todo.category == category)

    if due_date_from:
        query = query.filter(models.Todo.due_date >= due_date_from)

    if due_date_to:
        query = query.filter(models.Todo.due_date <= due_date_to)

    return query.offset(skip).limit(limit).all()
