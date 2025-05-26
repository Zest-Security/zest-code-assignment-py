import logging
import random
from datetime import datetime
from enum import Enum
from time import sleep

import counters
from app.core.config import TASK_MAX_RETRIES, TASK_SIMULATED_ERROR_PERCENTAGE, TASK_SIMULATED_DURATION, \
    TASK_ERROR_RETRY_DELAY
from app.models.task import TaskResponse, TaskStatistics

logger = logging.getLogger("task_processor")

class Statuses(Enum):
    IN_PROGRESS = 0
    SUCCESS = 1
    FAILED = 2


async def create_task(message: str) -> TaskResponse:
    """Create a new task and add it to the processing queue"""
    counters.task_id += 1
    task_id = "task_id=" + str(counters.task_id)
    message = "message=" + message
    retries = 0

    status = Statuses.IN_PROGRESS
    logger.info(f"Starting task #{counters.task_id}.")
    while retries <= TASK_MAX_RETRIES and status != Statuses.SUCCESS:
        counters.worker_id += 1
        if random.uniform(0, 1) > TASK_SIMULATED_ERROR_PERCENTAGE:
            worker_id = "worker_id=" + str(counters.worker_id)
            with open(r".\shared_file.log", 'a') as f:
                sleep(random.randrange(int(TASK_SIMULATED_DURATION) + 1))
                timestamp = "timestamp=" + datetime.now().isoformat()
                log = " ".join([str(timestamp), str(worker_id), str(task_id), message, "\n"])
                f.write(log)
                logger.info(f"Task #{counters.task_id}. Completed task successfully.")
                status = Statuses.SUCCESS
        else:
            logger.warning(f"Task #{counters.task_id} failed. Retrying in {TASK_ERROR_RETRY_DELAY} seconds.")
            status = Statuses.FAILED
            retries += 1
            sleep(TASK_ERROR_RETRY_DELAY)


    return TaskResponse(id=str(counters.task_id))


async def get_statistics() -> TaskStatistics:
    """Get current processing metrics"""
    raise Exception("Not implemented")
