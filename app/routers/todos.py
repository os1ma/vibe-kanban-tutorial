from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app import crud, models, schemas
from app.database import get_db

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[schemas.Todo])
def read_todos(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to retrieve"),
    db: Session = Depends(get_db),
):
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos


@router.get("/filter", response_model=List[schemas.Todo])
def filter_todos(
    status: Optional[str] = Query(
        None, pattern="^(open|in-progress|closed)$", description="Filter by status"
    ),
    priority: Optional[str] = Query(
        None, pattern="^(high|medium|low)$", description="Filter by priority"
    ),
    category: Optional[str] = Query(None, description="Filter by category"),
    due_date_from: Optional[datetime] = Query(
        None, description="Filter by due date from"
    ),
    due_date_to: Optional[datetime] = Query(None, description="Filter by due date to"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to retrieve"),
    db: Session = Depends(get_db),
):
    todos = crud.filter_todos(
        db,
        status=status,
        priority=priority,
        category=category,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        skip=skip,
        limit=limit,
    )
    return todos


@router.get("/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.post("/", response_model=schemas.Todo, status_code=201)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db=db, todo=todo)


@router.put("/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    db_todo = crud.update_todo(db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo


@router.delete("/{todo_id}", response_model=schemas.MessageResponse)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    success = crud.delete_todo(db, todo_id=todo_id)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": f"Todo with id {todo_id} has been deleted successfully"}
