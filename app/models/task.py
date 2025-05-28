from pydantic import BaseModel


class Task(BaseModel):
    message: str


class TaskResponse(BaseModel):
    id: str


class TaskStatistics(BaseModel):
    total_tasks: int
    tasks_processed: int
    task_retries: int
    tasks_succeeded: int
    tasks_failed: int
    success_to_fail_ratio: str
    average_duration: str
    queue_size: int
    number_of_workers: int
    idle_workers: int
    hot_workers: int
