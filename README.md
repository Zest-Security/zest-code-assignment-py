# Task Processing Microservice

A FastAPI application for processing tasks with a worker pool. Tasks are processed concurrently by a pool of workers, with each task being logged to a file.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables (optional):
```bash
# Create .env file with the following variables:
TASK_MAX_RETRIES=3        # Maximum number of retry attempts
TASK_ERROR_PERCENTAGE=30  # Percentage of tasks that will fail (0-100)
TASK_SIMULATED_DURATION=2000    # Processing time in milliseconds
SERVER_PORT=8000          # HTTP server port
```

3. Run the application:
```bash
# Option 1: Using the main script
python main.py

# Option 2: Using uvicorn directly
uvicorn main:app --reload --port $SERVER_PORT
```

The API will be available at `http://localhost:${SERVER_PORT}`

## Features

- Asynchronous task processing using a worker pool
- Concurrent task execution
- Task status tracking
- Processing statistics
- Logging of task processing to `task_processing.log`
- Configurable retry mechanism
- Random task failures for testing

## API Endpoints

### Create a Task
- **POST** `/tasks`
- Request body:
```json
{
    "message": "Task message to process"
}
```
- Example:
```bash
curl -X POST http://localhost:${SERVER_PORT}/tasks \
  -H "Content-Type: application/json" \
  -d '{"message": "Process this task"}'
```

### Get Task Status
- **GET** `/tasks/{task_id}`
- Returns the current status of a specific task
- Possible statuses: "pending", "completed", "failed", "retrying"
- Example:
```bash
curl http://localhost:${SERVER_PORT}/tasks/123e4567-e89b-12d3-a456-426614174000
```

### Get Statistics
- **GET** `/statistics`
- Returns live statistics about task processing including:
  - Total tasks
  - Completed tasks
  - Failed tasks
  - Currently processing tasks
  - Retried tasks
- Example:
```bash
curl http://localhost:${SERVER_PORT}/statistics
```

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:${SERVER_PORT}/docs`
- Alternative API documentation (ReDoc): `http://localhost:${SERVER_PORT}/redoc`

## Logging

Task processing logs are written to `task_processing.log` with the following information:
- Timestamp
- Process name
- Task ID
- Task message
- Processing status
- Retry attempts