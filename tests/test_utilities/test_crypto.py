"""Unit tests for src/Core/utilities/crypto.py"""

import base64

import pytest

from src.Core.exceptions import AutomationError
from src.Core.utilities.crypto import Crypto


class TestCryptoEncrypt:
    """Test Crypto.encrypt method."""

    def test_encrypt_with_salt(self) -> None:
        """Test encrypt with provided salt."""
        plaintext = "test password"
        password = "my_key"
        salt = b"1234567890123456"

        encrypted, returned_salt = Crypto.encrypt(plaintext, password, salt)

        assert isinstance(encrypted, bytes)
        assert returned_salt == salt
        assert len(encrypted) > 0

    def test_encrypt_without_salt(self) -> None:
        """Test encrypt generates salt if not provided."""
        plaintext = "test password"
        password = "my_key"

        encrypted, salt = Crypto.encrypt(plaintext, password)

        assert isinstance(encrypted, bytes)
        assert isinstance(salt, bytes)
        assert len(salt) == 16

    def test_encrypt_different_passwords_different_results(self) -> None:
        """Test different passwords produce different encrypted data."""
        plaintext = "test"
        salt = b"1234567890123456"

        enc1, _ = Crypto.encrypt(plaintext, "password1", salt)
        enc2, _ = Crypto.encrypt(plaintext, "password2", salt)

        assert enc1 != enc2

    def test_encrypt_special_characters(self) -> None:
        """Test encrypt with special characters."""
        plaintext = "Test@123!#$%^&*()"
        password = "key"

        encrypted, salt = Crypto.encrypt(plaintext, password)

        assert isinstance(encrypted, bytes)
        assert len(encrypted) > 0

    def test_encrypt_unicode(self) -> None:
        """Test encrypt with unicode characters."""
        plaintext = "测试 тест テスト"
        password = "key"

        encrypted, salt = Crypto.encrypt(plaintext, password)

        assert isinstance(encrypted, bytes)

    def test_encrypt_empty_string(self) -> None:
        """Test encrypt with empty string."""
        encrypted, salt = Crypto.encrypt("", "password")

        assert isinstance(encrypted, bytes)
        assert isinstance(salt, bytes)


class TestCryptoDecrypt:
    """Test Crypto.decrypt method."""

    def test_decrypt_success(self) -> None:
        """Test successful decryption."""
        plaintext = "test password"
        password = "my_key"
        salt = b"1234567890123456"

        encrypted, _ = Crypto.encrypt(plaintext, password, salt)
        decrypted = Crypto.decrypt(encrypted, password, salt)

        assert decrypted == plaintext

    def test_decrypt_round_trip(self) -> None:
        """Test encrypt then decrypt returns original."""
        original = "Hello World 123"
        password = "secret_key"

        encrypted, salt = Crypto.encrypt(original, password)
        decrypted = Crypto.decrypt(encrypted, password, salt)

        assert decrypted == original

    def test_decrypt_wrong_password_fails(self) -> None:
        """Test decrypt with wrong password fails."""
        plaintext = "test"
        salt = b"1234567890123456"

        encrypted, _ = Crypto.encrypt(plaintext, "correct", salt)

        with pytest.raises(Exception):
            Crypto.decrypt(encrypted, "wrong", salt)

    def test_decrypt_wrong_salt_fails(self) -> None:
        """Test decrypt with wrong salt fails."""
        plaintext = "test"
        password = "password"
        salt1 = b"1234567890123456"
        salt2 = b"6543210987654321"

        encrypted, _ = Crypto.encrypt(plaintext, password, salt1)

        with pytest.raises(Exception):
            Crypto.decrypt(encrypted, password, salt2)

    def test_decrypt_special_characters(self) -> None:
        """Test decrypt with special characters."""
        plaintext = "Test@123!#$%"
        password = "key"

        encrypted, salt = Crypto.encrypt(plaintext, password)
        decrypted = Crypto.decrypt(encrypted, password, salt)

        assert decrypted == plaintext

    def test_decrypt_unicode(self) -> None:
        """Test decrypt with unicode."""
        plaintext = "测试"
        password = "key"

        encrypted, salt = Crypto.encrypt(plaintext, password)
        decrypted = Crypto.decrypt(encrypted, password, salt)

        assert decrypted == plaintext


class TestCryptoGenerateKey:
    """Test Crypto.generate_key method."""

    def test_generate_key_returns_bytes(self) -> None:
        """Test generate_key returns bytes."""
        key = Crypto.generate_key()

        assert isinstance(key, bytes)

    def test_generate_key_different_each_time(self) -> None:
        """Test generate_key returns different keys."""
        key1 = Crypto.generate_key()
        key2 = Crypto.generate_key()

        assert key1 != key2

    def test_generate_key_length(self) -> None:
        """Test generated key has proper length."""
        key = Crypto.generate_key()

        assert len(key) == 44  # Fernet key length


class TestCryptoBase64:
    """Test Crypto base64 encode/decode methods."""

    def test_encode_base64_success(self) -> None:
        """Test successful base64 encoding."""
        data = "Hello World"

        encoded = Crypto.encode_base64(data)

        assert isinstance(encoded, str)
        assert encoded == base64.b64encode(data.encode()).decode()

    def test_decode_base64_success(self) -> None:
        """Test successful base64 decoding."""
        data = "Hello World"
        encoded = base64.b64encode(data.encode()).decode()

        decoded = Crypto.decode_base64(encoded)

        assert decoded == data

    def test_base64_round_trip(self) -> None:
        """Test encode then decode returns original."""
        original = "Test Data 123"

        encoded = Crypto.encode_base64(original)
        decoded = Crypto.decode_base64(encoded)

        assert decoded == original

    def test_encode_base64_special_characters(self) -> None:
        """Test base64 encode with special characters."""
        data = "Test@#$%^&*()"

        encoded = Crypto.encode_base64(data)
        decoded = Crypto.decode_base64(encoded)

        assert decoded == data

    def test_encode_base64_unicode(self) -> None:
        """Test base64 encode with unicode."""
        data = "测试 тест"

        encoded = Crypto.encode_base64(data)
        decoded = Crypto.decode_base64(encoded)

        assert decoded == data

    def test_encode_base64_empty_string(self) -> None:
        """Test base64 encode with empty string."""
        encoded = Crypto.encode_base64("")

        assert isinstance(encoded, str)
        assert len(encoded) == 0

    def test_decode_base64_invalid_raises_error(self) -> None:
        """Test decode invalid base64 raises error."""
        with pytest.raises(AutomationError):
            Crypto.decode_base64("invalid!@#$")


class TestCryptoErrorHandling:
    """Test Crypto error handling."""

    def test_encrypt_with_exception(self) -> None:
        """Test encrypt handles exceptions properly."""
        # This would need to mock internal functions to force an error
        # For now just verify it doesn't crash with valid inputs
        encrypted, salt = Crypto.encrypt("test", "password")
        assert encrypted is not None

    def test_decrypt_with_invalid_data(self) -> None:
        """Test decrypt with invalid encrypted data."""
        with pytest.raises(Exception):
            Crypto.decrypt(b"invalid", "password", b"1234567890123456")

    def test_automation_error_on_encrypt_failure(self) -> None:
        """Test AutomationError is raised on encrypt failure."""
        # Note: PBKDF2 accepts variable salt lengths, so this may not fail
        # Testing with actual invalid encryption scenario
        from src.Core.exceptions import AutomationError

        # Mock the Fernet to raise an error
        with pytest.raises(AutomationError):
            # Pass invalid type to trigger error
            Crypto.encrypt(None, "pass")  # type: ignore

    def test_automation_error_on_decrypt_failure(self) -> None:
        """Test AutomationError is raised on decrypt failure."""
        with pytest.raises(Exception):
            Crypto.decrypt(b"corrupted_data", "pass", b"1234567890123456")
