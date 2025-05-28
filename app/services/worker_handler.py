import asyncio
import logging
import multiprocessing

logger = logging.getLogger("worker_handler_logger")


class Worker:
    def __init__(self, id: int) -> None:
        self.id = id


class WorkerHandler:
    def __init__(self) -> None:
        core_count = multiprocessing.cpu_count()
        logger.info(f"Using {core_count} cores. Creating workers.")
        self._workers = [Worker(worker_id) for worker_id in range(1, core_count + 1)]
        self.worker_queue = asyncio.Queue(core_count)

    def prepare_workers(self) -> None:
        logger.info(f"Preparing workers. Inserting them into queue.")
        for worker in self._workers:
            self.worker_queue.put_nowait(worker)

    async def acquire_worker(self) -> Worker:
        worker = await self.worker_queue.get()
        logger.info(f"Worker {worker.id} acquired.")
        return worker

    async def release_worker(self, worker: Worker) -> None:
        await self.worker_queue.put(worker)
        logger.info(f"Worker {worker.id} released back to queue.")

    def get_max_workers(self) -> int:
        return self.worker_queue.maxsize

    def get_idle_workers_count(self) -> int:
        return self.worker_queue.qsize()

    def get_hot_workers_count(self) -> int:
        return self.worker_queue.maxsize - self.worker_queue.qsize()


worker_handler = WorkerHandler()
worker_handler.prepare_workers()
