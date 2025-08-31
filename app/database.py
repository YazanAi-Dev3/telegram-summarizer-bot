# app/database.py

import logging
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, select

logger = logging.getLogger(__name__)

DATABASE_URL = "sqlite:///database.db"
engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: int = Field(index=True)
    chat_id: int = Field(index=True)
    sender_name: str
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)

def create_db_and_tables():
    logger.info("Initializing the database and creating tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database and tables created successfully.")

def get_session():
    with Session(engine) as session:
        yield session

# --- NEW FUNCTION ---
def get_messages_in_range(session: Session, chat_id: int, start_message_id: int, end_message_id: int) -> List[Message]:
    """
    Queries the database to get all messages within a specific range in a specific chat.
    """
    logger.info(f"Querying database for messages in chat {chat_id} from {start_message_id} to {end_message_id}")
    
    statement = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .where(Message.message_id >= start_message_id)
        .where(Message.message_id <= end_message_id)
        .order_by(Message.timestamp) # Ensure chronological order
    )
    
    results = session.exec(statement).all()
    logger.info(f"Found {len(results)} messages in the database for the given range.")
    return results