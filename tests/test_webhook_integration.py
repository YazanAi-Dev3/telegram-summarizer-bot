# tests/test_webhook_integration.py

import pytest
from httpx import AsyncClient, ASGITransport
from app.webhook_handler import app

# We mark all tests in this file as asyncio tests
pytestmark = pytest.mark.asyncio

async def test_webhook_with_start_command(monkeypatch):
    """
    Tests the /webhook endpoint by simulating a /start command from Telegram.
    This is an integration test.
    """
    # This list will act as a "spy" to see what messages our bot tries to send.
    sent_messages = []
    
    async def mock_send_message(chat_id, text):
        sent_messages.append({"chat_id": chat_id, "text": text})
        return True # Simulate a successful send

    # Replace the real function with our mock function for the duration of this test
    monkeypatch.setattr("app.telegram_service.send_message", mock_send_message)

    # Prepare Fake Data for a /start command
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

    # Perform the Test Request
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/webhook", json=test_update)

    # Assert the Results
    assert response.status_code == 200
    assert len(sent_messages) == 1
    
    # Use the correct, up-to-date welcome message from logic_controller.py
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

    # Prepare Fake Data for a /help command
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
    # Check that the sent message contains a keyword from the help text
    assert "Here are the available commands" in sent_messages[0]["text"]