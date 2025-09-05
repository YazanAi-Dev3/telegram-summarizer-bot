# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Bot Token not found! Please set the BOT_TOKEN in your .env file.")

# Read the log level from the .env file, defaulting to "INFO" if not set.
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
# Read the summarizer mode, defaulting to "traditional" if not set.
# It can be "traditional" or "transformer"
SUMMARIZER_MODE = os.getenv("SUMMARIZER_MODE", "traditional")
DATABASE_URL = os.getenv("DATABASE_URL") 

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found! Please set it in your environment.")