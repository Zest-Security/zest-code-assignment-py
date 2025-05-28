import asyncio
import logging
import random
from enum import Enum

from app.core import counters
from app.core.config import TASK_MAX_RETRIES, TASK_SIMULATED_ERROR_PERCENTAGE, TASK_SIMULATED_DURATION, \
    TASK_ERROR_RETRY_DELAY
from app.models.task import TaskResponse, TaskStatistics
from app.services.worker_handler import worker_handler

task_logger = logging.getLogger("task_processor")


class Statuses(Enum):
    IN_PROGRESS = 0
    SUCCESS = 1
    FAILED = 2


def setup_shared_logging() -> logging.Logger:
    logger = logging.getLogger("shared_file_logger")

    shared_file_handler = logging.FileHandler(r"shared_file.log")
    shared_file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("timestamp=%(asctime)s "
                                  "worker_id=%(worker_id)s "
                                  "task_id=%(task_id)s "
                                  "message=%(message)s")
    shared_file_handler.setFormatter(formatter)

    logger.addHandler(shared_file_handler)
    logger.propagate = False

    return logger


shared_logger = setup_shared_logging()
shared_log_lock = asyncio.Lock()


async def wait_for_worker(task_id):
    await counters.add_to_current_queue_length()
    worker = await worker_handler.acquire_worker()
    await counters.remove_from_current_queue_length()
    task_logger.info(f"Starting task #{task_id}.")
    return worker


async def try_task(message, retries, task_id, worker_id):
    if random.uniform(0, 1) > TASK_SIMULATED_ERROR_PERCENTAGE:
        shared_logger.info(message, extra={"worker_id": worker_id, "task_id": task_id})
        task_logger.info(f"Task #{task_id}. Completed task successfully.")
        status = Statuses.SUCCESS
    else:
        retries += 1
        if retries <= TASK_MAX_RETRIES:
            task_logger.warning(f"Task #{task_id} failed. Retrying in {TASK_ERROR_RETRY_DELAY} seconds.")
            await counters.add_to_tasks_retries(retries)
            await asyncio.sleep(TASK_ERROR_RETRY_DELAY)
        else:
            task_logger.error(f"Task #{task_id} failed. Aborting task.")
        status = Statuses.FAILED
    return retries, status


async def create_task(message: str) -> TaskResponse:
    """Create a new task and add it to the processing queue"""
    task_id = await counters.get_next_task_id()
    retries = 0

    worker = await wait_for_worker(task_id)
    status = Statuses.IN_PROGRESS
    while retries <= TASK_MAX_RETRIES and status != Statuses.SUCCESS:
        async with shared_log_lock:
            proc_time = random.randrange(int(TASK_SIMULATED_DURATION) + 1)
            await counters.add_to_processing_times(proc_time)
            await asyncio.sleep(proc_time)
            retries, status = await try_task(message, retries, task_id, worker.id)

    await counters.add_to_success_count() if status == Statuses.SUCCESS else await counters.add_to_fail_count()
    await worker_handler.release_worker(worker)
    return TaskResponse(id=str(task_id))


async def get_statistics() -> TaskStatistics:
    """Get current processing metrics"""
    return TaskStatistics(
        total_tasks=counters.task_id.value,
        tasks_processed=counters.get_tasks_processed(),
        task_retries=counters.tasks_retries.value,
        tasks_succeeded=counters.success_count.value,
        tasks_failed=counters.fail_count.value,
        success_to_fail_ratio=counters.get_success_to_fail_ratio(),
        average_duration=str(counters.get_average_duration()),
        queue_size=counters.current_queue_length.value,
        number_of_workers=worker_handler.get_max_workers(),
        idle_workers=worker_handler.get_idle_workers_count(),
        hot_workers=worker_handler.get_hot_workers_count(),
    )
