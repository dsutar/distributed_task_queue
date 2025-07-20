import pytest
from httpx import AsyncClient
from task_api_service.main import app
from shared.database import init_db
import asyncio

@pytest.mark.asyncio
async def test_create_and_get_task():
    await init_db()
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create task
        response = await client.post("/tasks", json={"task_type": "echo", "payload": "hello"})
        assert response.status_code == 202
        task = response.json()
        assert task["id"] > 0
        task_id = task["id"]

        # Get task
        response = await client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["status"] == "pending"
