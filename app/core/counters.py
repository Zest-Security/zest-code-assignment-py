import asyncio
import logging
from datetime import timedelta
from typing import List, Union

logger = logging.getLogger("counters_logger")


class AsyncCounter:
    def __init__(self, initial_value: Union[int, List[int]]) -> None:
        self.value = initial_value
        self.lock = asyncio.Lock()

    async def increment(self, count: int = 1):
        async with self.lock:
            self.value += count

    async def deduct(self, count: int = 1) -> None:
        async with self.lock:
            self.value -= count

    async def append(self, duration: int) -> None:
        async with self.lock:
            self.value.append(duration)

    async def get_next(self):
        async with self.lock:
            self.value += 1
            return self.value


task_id = AsyncCounter(0)
tasks_retries = AsyncCounter(0)
success_count = AsyncCounter(0)
fail_count = AsyncCounter(0)
processing_times = AsyncCounter([])
current_queue_length = AsyncCounter(0)
idle_workers_count = AsyncCounter(0)
hot_workers_count = AsyncCounter(0)


async def get_next_task_id() -> int:
    return await task_id.get_next()


async def add_to_tasks_retries(count: int = 1) -> None:
    await tasks_retries.increment(count)


async def add_to_success_count(count: int = 1) -> None:
    await success_count.increment(count)


async def add_to_fail_count(count: int = 1) -> None:
    await fail_count.increment(count)


async def add_to_processing_times(duration: int) -> None:
    await processing_times.append(duration)


async def add_to_current_queue_length(count: int = 1) -> None:
    await current_queue_length.increment(count)


async def remove_from_current_queue_length(count: int = 1) -> None:
    await current_queue_length.deduct(count)


def get_tasks_processed() -> int:
    return success_count.value + fail_count.value


def get_average_duration() -> timedelta:
    if processing_times.value:
        average_duration = timedelta(seconds=sum(processing_times.value) / len(processing_times.value))
    else:
        average_duration = timedelta(seconds=0)
    return average_duration


def get_success_to_fail_ratio() -> str:
    percentage = round((success_count.value / fail_count.value) * 100, 2) if fail_count.value > 0 else 0
    return f"{success_count.value}:{fail_count.value} ({percentage}%)"
