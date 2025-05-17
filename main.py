import uvicorn
from fastapi import FastAPI

from app.models.task import Task, TaskResponse, TaskStatistics
from app.services.task_processor import create_task, get_statistics
from app.core.config import setup_logging, SERVER_PORT

# Setup logging
setup_logging()

app = FastAPI(title="Task Processing API")

@app.post("/tasks", response_model=TaskResponse)
async def create_task_endpoint(task: Task):
    task_data = await create_task(task.message)
    return task_data

@app.get("/statistics", response_model=TaskStatistics)
async def get_statistics_endpoint():
    return await get_statistics()

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT) 