from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
import enum
from sqlalchemy.sql import func
from app.database import Base


class TodoStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in-progress"
    CLOSED = "closed"


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TodoStatus), default=TodoStatus.OPEN, nullable=False)
    priority = Column(String(10), default="medium")
    category = Column(String(50), nullable=True)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
