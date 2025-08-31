# app/telegram_service.py

import logging
import asyncio
from telegram import Bot
from telegram.error import TelegramError
from app.config import BOT_TOKEN

logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)

async def send_message(chat_id: int, text: str) -> bool:
    """Sends a text message to a specified Telegram chat."""
    logger.info(f"Attempting to send message to chat_id: {chat_id}")
    try:
        # We use parse_mode='Markdown' to allow bold/italic text
        await bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')
        logger.info("Message sent successfully.")
        return True
    except TelegramError as e:
        logger.error(f"Failed to send message to {chat_id}. Error: {e}")
        return False

# --- Standalone Test Block --- (No changes needed here)
async def main_test():
    logger.info("--- Testing the Telegram Service Standalone ---")
    TEST_CHAT_ID = "YOUR_PERSONAL_CHAT_ID" 
    if TEST_CHAT_ID == "YOUR_PERSONAL_CHAT_ID":
        logger.error("Please replace 'YOUR_PERSONAL_CHAT_ID' with your actual chat ID to run the test.")
        return
    test_message = "Hello from the Summarizer Bot! If you see this, the Telegram service is working correctly. ✅"
    await send_message(chat_id=TEST_CHAT_ID, text=test_message)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    asyncio.run(main_test())