# app/webhook_handler.py

import logging
from contextlib import asynccontextmanager 
from fastapi import FastAPI, Request, Response, Depends
from sqlmodel import Session
from telegram import Update
from app.logic_controller import handle_update
from app.telegram_service import bot
from app.database import get_session, create_db_and_tables

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function runs once when the FastAPI application starts up.
    We use it to create our database tables.
    """
    logger.info("Application startup...")
    create_db_and_tables()
    yield
    # Code here would run on shutdown
    logger.info("Application shutdown...")

#
app = FastAPI(lifespan=lifespan)



@app.post("/webhook")
async def webhook(request: Request, session: Session = Depends(get_session)):
    
    logger.info("Webhook received a request.")
    try:
        data = await request.json()
        update = Update.de_json(data, bot)
        logger.debug(f"Update parsed successfully: {update.update_id}")
        await handle_update(update, session)
    except Exception as e:
        logger.error(f"Error processing webhook request: {e}", exc_info=True)
    finally:
        return Response(status_code=200)

@app.get("/")
def health_check():

    logger.info("Health check endpoint was accessed.")
    return {"status": "ok", "message": "Bot server is running"}