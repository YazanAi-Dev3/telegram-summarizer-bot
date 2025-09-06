# app/database.py

import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import Field, SQLModel, create_engine, Session, select, func, desc
from app.config import DATABASE_URL

logger = logging.getLogger(__name__)

# The engine connects to the DATABASE_URL from our config
engine = create_engine(DATABASE_URL, echo=False)

class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: int = Field(index=True)
    chat_id: int = Field(index=True)
    sender_name: str
    text: str
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)

def create_db_and_tables():
    """
    Initializes the database by creating all tables defined by SQLModel.
    """
    logger.info("Initializing the database and creating tables...")
    SQLModel.metadata.create_all(engine)
    logger.info("Database and tables created successfully.")

def get_session():
    """
    Dependency function to get a database session.
    """
    with Session(engine) as session:
        yield session

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

def get_chat_statistics(session: Session, chat_id: int) -> Dict[str, Any]:
    """
    Queries the database to get statistics for a specific chat.
    """
    logger.info(f"Querying database for statistics in chat {chat_id}")
    
    # Query 1: Total message count
    total_messages = session.exec(
        select(func.count(Message.id))
        .where(Message.chat_id == chat_id)
    ).one()
    
    # Query 2: Most active user
    most_active_user_result = session.exec(
        select(Message.sender_name, func.count(Message.id).label("message_count"))
        .where(Message.chat_id == chat_id)
        .group_by(Message.sender_name)
        .order_by(desc("message_count"))
        .limit(1)
    ).first()
    
    most_active_user = most_active_user_result[0] if most_active_user_result else "N/A"
    
    stats = {
        "total_messages": total_messages,
        "most_active_user": most_active_user
    }
    
    logger.info(f"Found stats for chat {chat_id}: {stats}")
    return stats

def get_last_n_messages(session: Session, chat_id: int, limit: int = 50) -> List[Message]:
    """
    Queries the database to get the last N messages from a specific chat.
    """
    logger.info(f"Querying database for the last {limit} messages in chat {chat_id}")
    
    statement = (
        select(Message)
        .where(Message.chat_id == chat_id)
        .order_by(desc(Message.timestamp)) # Get the newest messages first
        .limit(limit)
    )
    
    results = session.exec(statement).all()
    
    # The results are in reverse chronological order (newest to oldest),
    # so we reverse them back to the correct order (oldest to newest).
    results.reverse()
    
    logger.info(f"Found {len(results)} messages in the database.")
    return results