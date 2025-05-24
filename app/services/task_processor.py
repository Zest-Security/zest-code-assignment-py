import random
from datetime import datetime
from time import sleep
from app.core.config import TASK_MAX_RETRIES, TASK_SIMULATED_ERROR_PERCENTAGE, TASK_SIMULATED_DURATION, \
    TASK_ERROR_RETRY_DELAY
from app.models.task import TaskResponse, TaskStatistics
STATUSES = ["IN_QUEUE", "IN_PROGRESS", "SUCCESS", "FAILED"]


async def get_task_id() -> int:
    raise Exception("Not implemented")


async def get_worker_id() -> int:
    raise Exception("Not implemented")


async def create_task(message: str) -> TaskResponse:
    """Create a new task and add it to the processing queue"""
    task_id = get_task_id()
    status = STATUSES[0]
    retries = 0

    while retries <= TASK_MAX_RETRIES and status != STATUSES[3]:
        status = STATUSES[1]
        if random.uniform(0, 1) > TASK_SIMULATED_ERROR_PERCENTAGE:
            worker_id = get_worker_id()
            with open(r"C:\Windows\Temp\task_log.txt", 'a') as f:
                sleep(TASK_SIMULATED_DURATION)
                timestamp = datetime.now().timestamp()
                log = ", ".join([str(timestamp), str(worker_id), str(task_id), message])
                f.write(log)
                status = STATUSES[3]
        else:
            status = STATUSES[2]
            sleep(TASK_ERROR_RETRY_DELAY)

    return TaskResponse(id=task_id)


async def get_statistics() -> TaskStatistics:
    """Get current processing metrics"""
    raise Exception("Not implemented")
