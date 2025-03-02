import os
from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
from naomi_api.api import app
from tests.conftest import patch_session_scope


client = TestClient(app)


@pytest.fixture
def webhook_event_data():
    return {"type": "test_event", "payload": {"key": "value"}}


@patch("naomi_api.api.initialize_app")
@patch("naomi_api.api.credentials.Certificate")
def test_initialize_db_called(mock_certificate, mock_initialize_app):
    with patch("naomi_api.api.initialize_db") as mock_initialize_db:
        with TestClient(app):
            mock_initialize_db.assert_called_once()
            mock_certificate.assert_called_once()
            mock_initialize_app.assert_called_once()
    mock_initialize_db.assert_called_once()


def test_receive_webhook(webhook_event_data):
    with patch_session_scope("naomi_api.api.session_scope"):
        response = client.post("/webhook", json=webhook_event_data)
        assert response.status_code == 200
        assert response.json() == {"status": "OK"}


def test_serve_streamlit_wrapper():
    """Test the root endpoint that serves the streamlit wrapper HTML."""
    with patch(
        "pathlib.Path.read_text", return_value="<html>PLACEHOLDER_TEST content</html>"
    ), patch.dict(os.environ, {"TEST": "injected"}):

        response = client.get("/")

        assert response.status_code == 200
        assert response.headers["content-type"] == "text/html; charset=utf-8"
        assert "<html>injected content</html>" in response.text


def test_serve_firebase_messaging_sw():
    """Test the firebase-messaging-sw.js endpoint."""
    with patch(
        "pathlib.Path.read_text", return_value="console.log('PLACEHOLDER_APP_ID');"
    ), patch.dict(os.environ, {"APP_ID": "test-app-123"}):

        response = client.get("/firebase-messaging-sw.js")

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/javascript"
        assert "console.log('test-app-123');" in response.text
