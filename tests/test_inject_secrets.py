import os
from unittest.mock import patch

import pytest

from naomi_api.inject_secrets import PlaceholderInjector


@pytest.fixture
def injector():
    return PlaceholderInjector()


@pytest.mark.parametrize(
    "content,env_vars,expected,default",
    [
        # Standard placeholder replacement
        (
            "API Key: PLACEHOLDER_API_KEY",
            {"API_KEY": "test-key-123"},
            "API Key: test-key-123",
            "",
        ),
        # Multiple placeholders
        (
            "API: PLACEHOLDER_API_KEY, Project: PLACEHOLDER_PROJECT_ID",
            {"API_KEY": "key-123", "PROJECT_ID": "proj-456"},
            "API: key-123, Project: proj-456",
            "",
        ),
        # Default value for missing env var
        (
            "Missing: PLACEHOLDER_MISSING",
            {},
            "Missing: not-set",
            "not-set",
        ),
    ],
)
def test_inject_basic_cases(injector, content, env_vars, expected, default):
    with patch.dict(os.environ, env_vars):
        result = injector.inject(content, default_value=default)
        assert result == expected


def test_inject_with_custom_mapping(injector):
    injector.add_custom_mapping("API_KEY", "FIREBASE_API_KEY")
    with patch.dict(os.environ, {"FIREBASE_API_KEY": "firebase-key"}):
        result = injector.inject("API Key: PLACEHOLDER_API_KEY")
        assert result == "API Key: firebase-key"


def test_inject_with_custom_pattern():
    custom_injector = PlaceholderInjector(placeholder_pattern=r"SECRET_([A-Z0-9_]+)")
    with patch.dict(os.environ, {"API_KEY": "secret-value"}):
        result = custom_injector.inject("API Key: SECRET_API_KEY")
        assert result == "API Key: secret-value"
