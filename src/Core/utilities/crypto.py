import base64
from typing import Optional, Tuple

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from src.Core import AutomationError, auto_log


class Crypto:
    @staticmethod
    @auto_log
    def encrypt(
        plaintext: str, password: str, salt: Optional[bytes] = None
    ) -> Tuple[bytes, bytes]:
        try:
            if salt is None:
                salt = Fernet.generate_key()[:16]

            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=120000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

            # Encrypt data
            fernet = Fernet(key)
            encrypted_data = fernet.encrypt(plaintext.encode())

            return encrypted_data, salt
        except Exception as e:
            raise AutomationError("Failed to encrypt data", str(e)) from e

    @staticmethod
    @auto_log
    def decrypt(encrypted_data: bytes, password: str, salt: bytes) -> str:
        try:
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=120000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))

            # Decrypt data
            fernet = Fernet(key)
            decrypted_data = fernet.decrypt(encrypted_data)

            plaintext = decrypted_data.decode()
            return plaintext
        except Exception as e:
            raise AutomationError("Failed to decrypt data", str(e)) from e

    @staticmethod
    @auto_log
    def generate_key() -> bytes:
        try:
            key = Fernet.generate_key()
            return key
        except Exception as e:
            raise AutomationError("Failed to generate key", str(e)) from e

    @staticmethod
    @auto_log
    def encode_base64(data: str) -> str:
        try:
            encoded = base64.b64encode(data.encode()).decode()
            return encoded
        except Exception as e:
            raise AutomationError("Failed to encode base64", str(e)) from e

    @staticmethod
    @auto_log
    def decode_base64(encoded_data: str) -> str:
        try:
            decoded = base64.b64decode(encoded_data.encode()).decode()
            return decoded
        except Exception as e:
            raise AutomationError("Failed to decode base64", str(e)) from e
