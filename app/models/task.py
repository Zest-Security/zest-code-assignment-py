from pydantic import BaseModel
from datetime import datetime

class Task(BaseModel):
    message: str

class TaskResponse(BaseModel):
    id: str

class TaskStatistics(BaseModel):
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    average_duration: float
    retry_tasks: int
    queue_size: int
    number_of_workers: int