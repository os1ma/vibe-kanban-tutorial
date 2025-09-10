from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TodoBase(BaseModel):
    title: str = Field(..., max_length=100, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    priority: str = Field("medium", pattern="^(high|medium|low)$", description="Task priority")
    category: Optional[str] = Field(None, max_length=50, description="Task category")
    due_date: Optional[datetime] = Field(None, description="Due date")

class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[bool] = Field(None, description="Completion status")
    priority: Optional[str] = Field(None, pattern="^(high|medium|low)$", description="Task priority")
    category: Optional[str] = Field(None, max_length=50, description="Task category")
    due_date: Optional[datetime] = Field(None, description="Due date")

class Todo(TodoBase):
    id: int
    status: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    message: str