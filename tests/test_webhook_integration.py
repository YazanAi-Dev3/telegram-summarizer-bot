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
    
    # --- THE IMPORTANT CHANGE IS HERE ---
    # We now check for each piece of data independently. This is more robust.
    final_message = sent_messages[0]
    assert "Total Archived Messages" in final_message
    assert "125" in final_message
    assert "Most Active User" in final_message
    assert "TestUser" in final_message