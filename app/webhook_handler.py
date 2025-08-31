# app/webhook_handler.py

import logging
from fastapi import FastAPI, Request, Response, Depends
from sqlmodel import Session
from telegram import Update
from app.logic_controller import handle_update
from app.telegram_service import bot
from app.database import get_session

logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request, session: Session = Depends(get_session)):
    """
    Receives updates from Telegram, gets a database session,
    and passes them to the logic controller.
    """
    logger.info("Webhook received a request.")
    try:
        data = await request.json()
        update = Update.de_json(data, bot)
        logger.debug(f"Update parsed successfully: {update.update_id}")
        
        # Pass both the update and the database session to the handler
        await handle_update(update, session)
        
    except Exception as e:
        logger.error(f"Error processing webhook request: {e}", exc_info=True)
        
    finally:
        return Response(status_code=200)

@app.get("/")
def health_check():
    """A simple health check endpoint."""
    logger.info("Health check endpoint was accessed.")
    return {"status": "ok", "message": "Bot server is running"}