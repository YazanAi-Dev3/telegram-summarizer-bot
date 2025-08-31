# app/logic_controller.py
from telegram.helpers import escape_markdown
import logging
from telegram import Update
from sqlmodel import Session
from app import summarization_service, telegram_service
from app.database import Message, get_messages_in_range # Import the new function

logger = logging.getLogger(__name__)

async def handle_update(update: Update, session: Session):
    """
    Handles incoming updates, saves the message, and processes commands.
    """
    if not update.message or not update.message.text:
        logger.debug("Received an update without a message or text, ignoring.")
        return

    # --- Step 1: Archive the incoming message (No changes here) ---
    try:
        new_message = Message(
            message_id=update.message.message_id,
            chat_id=update.message.chat_id,
            sender_name=update.message.from_user.first_name,
            text=update.message.text,
            timestamp=update.message.date
        )
        session.add(new_message)
        session.commit()
        session.refresh(new_message)
        logger.info(f"Saved message {new_message.message_id} from {new_message.sender_name} to the database.")
    except Exception as e:
        logger.error(f"Failed to save message to database: {e}")
        session.rollback()

    # --- Step 2: Handle Commands ---
    chat_id = update.message.chat_id
    text = update.message.text

    if text.lower().startswith("/start"):
        welcome_message = "Welcome! To summarize a conversation, reply to the **starting message** with the `/summarize` command."
        await telegram_service.send_message(chat_id, welcome_message)
        return

    if text.lower().startswith("/summarize"):
        if update.message.reply_to_message:
            
            start_id = update.message.reply_to_message.message_id
            end_id = update.message.message_id
            
            await telegram_service.send_message(chat_id, "Got it! Searching the archive for your conversation... ⏳")
            
            # 1. Fetch the list of message objects from the database
            message_objects = get_messages_in_range(session, chat_id, start_id, end_id)
            
            if not message_objects:
                await telegram_service.send_message(chat_id, "I couldn't find any messages in the archive for this range.")
                return
            
            # 2. Format the messages into a list of strings for the summarizer
            # This adds the speaker's name for context
            messages_to_summarize = [f"{msg.sender_name}: {msg.text}" for msg in message_objects]

            # 3. Call the summarization service
            summary = summarization_service.create_summary(messages_to_summarize)
            
            sanitized_summary = escape_markdown(summary, version=2) 
            
            await telegram_service.send_message(chat_id, f"**Summary of the conversation:**\n\n{sanitized_summary}")
            # 4. Send the final summary
        else:
            error_message = "Please **reply** to the first message of the conversation you want to summarize."
            await telegram_service.send_message(chat_id, error_message)
        return