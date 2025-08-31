# app/webhook_handler.py

import logging
from fastapi import FastAPI, Request, Response, Depends
from sqlmodel import Session
from telegram import Update
from app.logic_controller import handle_update
from app.telegram_service import bot
from app.database import get_session, create_db_and_tables # <-- 1. استيراد الدالة

logger = logging.getLogger(__name__)

app = FastAPI()

# --- THE IMPORTANT CHANGE IS HERE ---
@app.on_event("startup")
def on_startup():
    """
    This function runs once when the FastAPI application starts.
    We use it to create our database tables.
    """
    create_db_and_tables()

@app.post("/webhook")
async def webhook(request: Request, session: Session = Depends(get_session)):
    # ... (rest of the code is the same)
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
    # ... (rest of the code is the same)
    logger.info("Health check endpoint was accessed.")
    return {"status": "ok", "message": "Bot server is running"}