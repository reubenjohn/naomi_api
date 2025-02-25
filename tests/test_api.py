from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from naomi_api.api import app
from tests.conftest import patch_session_scope


client = TestClient(app)


@pytest.fixture
def webhook_event_data():
    return {"type": "test_event", "payload": {"key": "value"}}


def test_initialize_db_called():
    with patch("naomi_api.api.initialize_db") as mock_initialize_db:
        with TestClient(app):
            mock_initialize_db.assert_called_once()
    mock_initialize_db.assert_called_once()


def test_receive_webhook(webhook_event_data):
    with patch_session_scope("naomi_api.api.session_scope"):
        response = client.post("/webhook", json=webhook_event_data)
        assert response.status_code == 200
        assert response.json() == {"status": "OK"}
