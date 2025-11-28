"""Utilities module specific fixtures."""

import pytest


@pytest.fixture
def mock_crypto_data() -> dict:
    """Sample crypto test data."""
    return {
        "plaintext": "test password 123",
        "password": "encryption_key",
        "salt": b"test_salt_16byte",
    }
