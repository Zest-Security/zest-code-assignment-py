# Task Processing API

A FastAPI-based service for processing tasks with simulated processing time and error handling.

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Task processing configuration
TASK_MAX_RETRIES=3                    # Maximum number of retries for failed tasks
TASK_SIMULATED_ERROR_PERCENTAGE=30    # Percentage of tasks that will fail (0-100)
TASK_SIMULATED_DURATION=2000          # Simulated processing duration in milliseconds
TASK_ERROR_RETRY_DELAY=2000          # Delay between retries in milliseconds

# Server configuration
SERVER_PORT=8000                      # Port number for the API server
```

## API Endpoints

### Health Check
- **GET** `/health`
  - Returns the health status of the API
  - Response: `{"status": "healthy"}`

### Task Processing
- **POST** `/tasks`
  - Creates and processes a new task
  - Request body: `{"message": "string"}`
  - Response: Task processing result

### Statistics
- **GET** `/statistics`
  - Returns task processing statistics
  - Response: Task statistics including success/failure counts

## Running the Application

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python main.py
```

The API will be available at `http://localhost:8000` (or the port specified in your environment variables).

## API Documentation

Once the server is running, you can access:
- Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
- Alternative API documentation (ReDoc): `http://localhost:8000/redoc`