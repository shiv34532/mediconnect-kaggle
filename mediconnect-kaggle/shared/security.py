"""
Shared Security Utilities
=========================
Demonstrates: Security features (encryption, data handling)

Provides encryption and secure data handling utilities used across
all agents in the MediConnect system.
"""
from cryptography.fernet import Fernet
import os
import base64


class SecureDataHandler:
    """
    Handles encryption and secure data operations.

    Uses Fernet symmetric encryption (AES-128 in CBC mode with PKCS7 padding)
    for securing sensitive data at rest and in transit.

    Attributes:
        key: Encryption key (loaded from environment or generated)
        cipher: Fernet cipher instance for encryption/decryption
    """

    def __init__(self, key: str = None):
        """
        Initialize the secure data handler.

        Args:
            key: Optional encryption key. If not provided, loads from
                 ENCRYPTION_KEY environment variable or generates new key.
        """
        if key:
            self.key = key.encode() if isinstance(key, str) else key
        else:
            env_key = os.getenv("ENCRYPTION_KEY")
            if env_key:
                self.key = env_key.encode() if isinstance(env_key, str) else env_key
            else:
                # Generate new key (for demo only - in production, always use env var)
                self.key = Fernet.generate_key()
                print("[WARNING] Generated new encryption key. Store this securely!")
                print(f"Key: {self.key.decode()}")

        self.cipher = Fernet(self.key)

    def encrypt(self, data: str) -> str:
        """
        Encrypt sensitive data string.

        Args:
            data: Plain text string to encrypt

        Returns:
            Base64-encoded encrypted token

        Example:
            >>> handler = SecureDataHandler()
            >>> encrypted = handler.encrypt("sensitive patient data")
        """
        token = self.cipher.encrypt(data.encode("utf-8"))
        return token.decode("utf-8")

    def decrypt(self, token: str) -> str:
        """
        Decrypt data (only for authorized agents with key access).

        Args:
            token: Encrypted token string

        Returns:
            Decrypted plain text string

        Example:
            >>> handler = SecureDataHandler()
            >>> decrypted = handler.decrypt(encrypted_token)
        """
        data = self.cipher.decrypt(token.encode("utf-8"))
        return data.decode("utf-8")

    def mask_pii(self, text: str, mask_char: str = "*") -> str:
        """
        Mask PII in text output by replacing sensitive parts.

        Args:
            text: Text containing potential PII
            mask_char: Character to use for masking (default: *)

        Returns:
            Text with PII masked
        """
        import re

        # Mask phone numbers: 555-123-4567 -> ***-***-****
        text = re.sub(
            r'\d{3}[-.]\d{3}[-.]\d{4}',
            lambda m: mask_char * 3 + "-" + mask_char * 3 + "-" + mask_char * 4,
            text
        )

        # Mask SSN: 123-45-6789 -> ***-**-****
        text = re.sub(
            r'\d{3}-\d{2}-\d{4}',
            lambda m: mask_char * 3 + "-" + mask_char * 2 + "-" + mask_char * 4,
            text
        )

        # Mask email: user@domain.com -> ****@domain.com
        text = re.sub(
            r'([A-Za-z0-9._%+-])@',
            lambda m: mask_char + "@",
            text
        )

        return text

    def hash_identifier(self, identifier: str) -> str:
        """
        Create a one-way hash of an identifier.

        Args:
            identifier: String to hash (e.g., patient name, phone)

        Returns:
            SHA-256 hash truncated to 16 characters
        """
        import hashlib
        return hashlib.sha256(identifier.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    # Demo
    print("=" * 60)
    print("Secure Data Handler - Demo")
    print("=" * 60)

    handler = SecureDataHandler()

    # Test encryption
    print("\n1. Encryption/Decryption:")
    sensitive_data = "Patient has diabetes, hypertension"
    encrypted = handler.encrypt(sensitive_data)
    print(f"   Original: {sensitive_data}")
    print(f"   Encrypted: {encrypted[:50]}...")
    decrypted = handler.decrypt(encrypted)
    print(f"   Decrypted: {decrypted}")
    print(f"   Match: {sensitive_data == decrypted}")

    # Test masking
    print("\n2. PII Masking:")
    text_with_pii = "Contact patient at 555-123-4567 or email john@email.com. SSN: 123-45-6789"
    masked = handler.mask_pii(text_with_pii)
    print(f"   Original: {text_with_pii}")
    print(f"   Masked:   {masked}")

    # Test hashing
    print("\n3. Identifier Hashing:")
    name = "Maria Garcia"
    hash_val = handler.hash_identifier(name)
    print(f"   Name: {name}")
    print(f"   Hash: {hash_val}")

    print("\n" + "=" * 60)
