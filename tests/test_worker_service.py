import pytest
from httpx import AsyncClient
from worker_service.main import app
from task_api_service.main import app as task_app
from shared.database import init_db
from shared.models import TaskType
import asyncio

@pytest.mark.asyncio
async def test_worker_process_task():
    # Initialize DB
    await init_db()

    # Create task in the API
    async with AsyncClient(app=task_app, base_url="http://test") as client:
        response = await client.post("/tasks", json={"task_type": "reverse_string", "payload": "hello"})
        assert response.status_code == 202
        task_id = response.json()["id"]

    # Process task via worker
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/process-task", json={"task_id": task_id})
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    # Re-check the task
    async with AsyncClient(app=task_app, base_url="http://test") as client:
        response = await client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "completed"
        assert data["result"] == "olleh"
