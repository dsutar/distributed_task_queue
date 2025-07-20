from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from shared.models import Task, TaskStatus, TaskType
from shared.database import get_session
from pydantic import BaseModel
import os
import httpx

router = APIRouter()

class TaskRequest(BaseModel):
    task_type: TaskType
    payload: str

class TaskResponse(BaseModel):
    id: int
    status: TaskStatus
    result: str | None

    class Config:
        orm_mode = True

@router.post("/tasks", response_model=TaskResponse, status_code=202)
async def create_task(request: TaskRequest, session: AsyncSession = Depends(get_session)):
    task = Task(task_type=request.task_type, payload=request.payload)
    session.add(task)
    await session.commit()
    await session.refresh(task)

    try:
        async with httpx.AsyncClient() as client:
            await client.post(os.getenv("WORKER_URL", "http://localhost:8001") + "/process-task", json={"task_id": task.id})
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to contact worker service.")

    return task

@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
