import asyncio
import logging
import random
from enum import Enum

import counters
from app.core.config import TASK_MAX_RETRIES, TASK_SIMULATED_ERROR_PERCENTAGE, TASK_SIMULATED_DURATION, \
    TASK_ERROR_RETRY_DELAY
from app.models.task import TaskResponse, TaskStatistics

task_logger = logging.getLogger("task_processor")


def setup_shared_logging() -> logging.Logger:
    shared_logger = logging.getLogger("shared_file_logger")

    shared_file_handler = logging.FileHandler(r"shared_file.log")
    shared_file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("timestamp=%(asctime)s "
                                  "worker_id=%(worker_id)s "
                                  "task_id=%(task_id)s "
                                  "message=%(message)s")
    shared_file_handler.setFormatter(formatter)

    shared_logger.addHandler(shared_file_handler)
    shared_logger.propagate = False

    return shared_logger


shared_logger = setup_shared_logging()


class Statuses(Enum):
    IN_PROGRESS = 0
    SUCCESS = 1
    FAILED = 2


task_id_lock = asyncio.Lock()
worker_id_lock = asyncio.Lock()
shared_log_lock = asyncio.Lock()


async def get_next_task_id():
    async with task_id_lock:
        counters.task_id += 1
        return counters.task_id


async def get_next_worker_id():
    async with worker_id_lock:
        counters.worker_id += 1
        return counters.worker_id


async def try_task(message, retries, task_id, worker_id):
    if random.uniform(0, 1) > TASK_SIMULATED_ERROR_PERCENTAGE:
        shared_logger.info(message, extra={"worker_id": worker_id, "task_id": task_id})
        task_logger.info(f"Task #{task_id}. Completed task successfully.")
        status = Statuses.SUCCESS
    else:
        retries += 1
        if retries != TASK_MAX_RETRIES:
            task_logger.warning(f"Task #{task_id} failed. Retrying in {TASK_ERROR_RETRY_DELAY} seconds.")
        else:
            task_logger.error(f"Task #{task_id} failed. Aborting task.")
        status = Statuses.FAILED
    return retries, status


async def create_task(message: str) -> TaskResponse:
    """Create a new task and add it to the processing queue"""
    task_id = await get_next_task_id()
    retries = 0

    status = Statuses.IN_PROGRESS
    task_logger.info(f"Starting task #{task_id}.")
    while retries <= TASK_MAX_RETRIES and status != Statuses.SUCCESS:
        worker_id = await get_next_worker_id()
        async with shared_log_lock:
            await asyncio.sleep(random.randrange(int(TASK_SIMULATED_DURATION) + 1))
            retries, status = await try_task(message, retries, task_id, worker_id)

        if retries != TASK_MAX_RETRIES:
            await asyncio.sleep(TASK_ERROR_RETRY_DELAY)

    return TaskResponse(id=str(task_id))


async def get_statistics() -> TaskStatistics:
    """Get current processing metrics"""
    raise Exception("Not implemented")
