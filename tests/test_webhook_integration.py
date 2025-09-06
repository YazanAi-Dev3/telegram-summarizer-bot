# tests/test_webhook_integration.py

import pytest
from httpx import AsyncClient, ASGITransport
from app.webhook_handler import app

# We mark all tests in this file as asyncio tests
pytestmark = pytest.mark.asyncio

async def test_webhook_with_start_command(monkeypatch):
    """
    Tests the /webhook endpoint by simulating a /start command from Telegram.
    """
    sent_messages = []
    
    async def mock_send_message(chat_id, text):
        sent_messages.append({"chat_id": chat_id, "text": text})
        return True

    monkeypatch.setattr("app.telegram_service.send_message", mock_send_message)

    test_update = {
        "update_id": 12345,
        "message": {
            "message_id": 67890,
            "date": 1678886400,
            "chat": {"id": -100123, "type": "group", "title": "Test Group"},
            "from": {"id": 54321, "is_bot": False, "first_name": "TestUser"},
            "text": "/start"
        }
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/webhook", json=test_update)

    assert response.status_code == 200
    assert len(sent_messages) == 1
    
    welcome_message = "Welcome! To summarize a conversation, reply to the **starting message** with the `/summarize` command."
    assert sent_messages[0]["chat_id"] == -100123
    assert sent_messages[0]["text"] == welcome_message


async def test_webhook_with_help_command(monkeypatch):
    """Tests the /webhook endpoint by simulating a /help command."""
    sent_messages = []
    
    async def mock_send_message(chat_id, text):
        sent_messages.append({"chat_id": chat_id, "text": text})
        return True

    monkeypatch.setattr("app.telegram_service.send_message", mock_send_message)

    test_update = {
        "update_id": 12346,
        "message": {
            "message_id": 67891,
            "date": 1678886401,
            "chat": {"id": -100123, "type": "group", "title": "Test Group"},
            "from": {"id": 54321, "is_bot": False, "first_name": "TestUser"},
            "text": "/help"
        }
    }
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/webhook", json=test_update)

    assert response.status_code == 200
    assert len(sent_messages) == 1
    assert "Here are the available commands" in sent_messages[0]["text"]


async def test_webhook_with_stats_command(monkeypatch):
    """Tests the /webhook endpoint by simulating a /stats command."""
    # 1. Mock the database function to return predictable data
    def mock_get_stats(session, chat_id):
        return {"total_messages": 125, "most_active_user": "TestUser"}
    
    monkeypatch.setattr("app.logic_controller.get_chat_statistics", mock_get_stats)

    # 2. Mock the send_message function
    sent_messages = []
    async def mock_send_message(chat_id, text):
        sent_messages.append(text)
        return True
    
    monkeypatch.setattr("app.telegram_service.send_message", mock_send_message)

    # 3. Prepare the fake update
    test_update = {
        "update_id": 12347,
        "message": {
            "message_id": 67892,
            "date": 1678886402,
            "chat": {"id": -100123, "type": "group", "title": "Test Group"},
            "from": {"id": 54321, "is_bot": False, "first_name": "TestUser"},
            "text": "/stats"
        }
    }
    
    # 4. Perform the request
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/webhook", json=test_update)

    # 5. Assert the results
    assert response.status_code == 200
    assert len(sent_messages) == 1
    final_message = sent_messages[0]
    assert "Total Archived Messages" in final_message
    assert "125" in final_message
    assert "Most Active User" in final_message
    assert "TestUser" in final_message


async def test_webhook_with_summarize_last_command(monkeypatch):
    """Tests the /webhook endpoint for the /summarize_last command."""
    # 1. Mock the database function
    retrieved_messages = []
    def mock_get_last_n(session, chat_id, limit):
        nonlocal retrieved_messages
        # Simulate returning 'limit' number of message objects
        class MockMessage:
            def __init__(self, sender, text):
                self.sender_name = sender
                self.text = text
        retrieved_messages = [MockMessage("User", f"Message {i}") for i in range(limit)]
        return retrieved_messages
    
    monkeypatch.setattr("app.logic_controller.get_last_n_messages", mock_get_last_n)

    # 2. Mock the summarization service
    def mock_create_summary(messages):
        return f"This is a summary of {len(messages)} messages."
    
    monkeypatch.setattr("app.logic_controller.summarization_service.create_summary", mock_create_summary)
    
    # 3. Mock the send_message function
    sent_messages_to_user = []
    async def mock_send_message(chat_id, text):
        sent_messages_to_user.append(text)
        return True
    
    monkeypatch.setattr("app.telegram_service.send_message", mock_send_message)

    # 4. Prepare and perform the request
    test_update = {
        "update_id": 12348,
        "message": { "message_id": 67893, "date": 1678886403,
            "chat": {"id": -100123, "type": "group", "title": "Test Group"},
            "from": {"id": 54321, "is_bot": False, "first_name": "TestUser"},
            "text": "/summarize_last 25"
        }
    }
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        await client.post("/webhook", json=test_update)

    # 5. Assert the results
    # The bot sends two messages: an acknowledgment and the summary
    assert len(sent_messages_to_user) == 2
    assert "Got it! Summarizing the last 25 messages" in sent_messages_to_user[0]
    assert "This is a summary of 25 messages." in sent_messages_to_user[1]