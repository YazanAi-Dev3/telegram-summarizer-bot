# main.py

import uvicorn
import logging
from app.logging_config import setup_logging

# It's crucial to set up logging BEFORE importing other app modules
setup_logging()

# Import the database creation function
from app.database import create_db_and_tables

# Now, we import the FastAPI app object from our webhook handler
from app.webhook_handler import app

logger = logging.getLogger(__name__)

# Create the database and tables before the app starts
create_db_and_tables()

if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run("app.webhook_handler:app", host="0.0.0.0", port=8000, reload=True)