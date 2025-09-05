# tests/test_webhook_integration.py

import pytest
from httpx import AsyncClient, ASGITransport
from app.webhook_handler import app

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
    
    # This is the correct, up-to-date welcome message from logic_controller.py
    welcome_message = "Welcome! To summarize a conversation, reply to the **starting message** with the `/summarize` command."
    
    assert sent_messages[0]["chat_id"] == -100123
    assert sent_messages[0]["text"] == welcome_message