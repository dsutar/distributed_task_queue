from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.future import select
from shared.database import get_session
from shared.models import Task, TaskStatus, TaskType
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
import asyncio

router = APIRouter()

class TaskProcessRequest(BaseModel):
    task_id: int

@router.post("/process-task")
async def process_task(payload: TaskProcessRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.id == payload.task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.status = TaskStatus.in_progress
    try:
        if task.task_type == TaskType.echo:
            task.result = task.payload
        elif task.task_type == TaskType.reverse_string:
            task.result = task.payload[::-1]
        elif task.task_type == TaskType.cpu_intensive:
            await asyncio.sleep(10)
            task.result = "CPU Task Done"
        task.status = TaskStatus.completed
    except Exception as e:
        task.status = TaskStatus.failed
        task.result = str(e)

    await session.commit()
    return {"status": task.status}
