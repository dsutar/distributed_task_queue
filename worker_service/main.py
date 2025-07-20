from fastapi import FastAPI
from worker_service.routes import router
from shared.database import init_db

app = FastAPI(title="Worker Service")

@app.on_event("startup")
async def startup():
    await init_db()

app.include_router(router)
