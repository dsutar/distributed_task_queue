from sqlalchemy import Column, Integer, String, Enum, Text
from sqlalchemy.orm import declarative_base
import enum

Base = declarative_base()

class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"

class TaskType(str, enum.Enum):
    echo = "echo"
    reverse_string = "reverse_string"
    cpu_intensive = "cpu_intensive"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_type = Column(Enum(TaskType), nullable=False)
    payload = Column(Text, nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending)
    result = Column(Text, nullable=True)
