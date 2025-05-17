import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Task processing configuration
TASK_MAX_RETRIES = int(os.getenv('TASK_MAX_RETRIES', '3'))
TASK_SIMULATED_ERROR_PERCENTAGE = float(os.getenv('TASK_SIMULATED_ERROR_PERCENTAGE', '30')) / 100
TASK_SIMULATED_DURATION = int(os.getenv('TASK_SIMULATED_DURATION', '2000')) / 1000
TASK_ERROR_RETRY_DELAY = int(os.getenv('TASK_ERROR_RETRY_DELAY', '2000')) / 1000

# Server configuration
SERVER_PORT = int(os.getenv('SERVER_PORT', '8000'))

def setup_logging():
    """Configure logging for the application"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(processName)s - %(message)s',
        handlers=[
            logging.FileHandler('task_processing.log'),
            logging.StreamHandler()
        ]
    ) 