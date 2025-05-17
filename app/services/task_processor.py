from app.models.task import TaskResponse, TaskStatistics

async def create_task(message: str) -> TaskResponse:
    """Create a new task and add it to the processing queue"""
    raise Exception("Not implemented")

async def get_statistics() -> TaskStatistics:
    """Get current processing metrics"""
    raise Exception("Not implemented")