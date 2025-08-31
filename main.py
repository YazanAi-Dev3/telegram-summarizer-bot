# main.py

import uvicorn
import logging
from app.logging_config import setup_logging

# Set up logging before anything else
setup_logging()

# Import the FastAPI app object
from app.webhook_handler import app

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    logger.info("Starting Uvicorn server for local development...")
    uvicorn.run("app.webhook_handler:app", host="0.0.0.0", port=8000, reload=True)