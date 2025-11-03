import base64
from dataclasses import dataclass
from typing import Tuple

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


# -------------------- Diffie-Hellman core --------------------

def compute_public_key(g: int, private_key: int, p: int) -> int:
    return pow(g, private_key, p)


def compute_shared_secret(other_public: int, private_key: int, p: int) -> int:
    return pow(other_public, private_key, p)


# -------------------- Key Derivation for Symmetric Encryption --------------------


def derive_symmetric_key(shared_secret: int, p: int, g: int) -> bytes:
    """
    Derive a 32-byte key from the DH shared secret using HKDF-SHA256.
    The result is then converted to a Fernet-compatible base64 key.
    """
    # Represent shared secret as bytes in big-endian
    secret_bytes = shared_secret.to_bytes((shared_secret.bit_length() + 7) // 8 or 1, "big")

    # Use (p, g) as part of salt to namespace different parameter sets
    salt = (str(p) + ":" + str(g)).encode()

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        info=b"diffie-hellman-demo",
    )
    key_material = hkdf.derive(secret_bytes)
    # Fernet requires URL-safe base64 32-byte key
    fernet_key = base64.urlsafe_b64encode(key_material)
    return fernet_key


# -------------------- Encryption helpers --------------------

@dataclass
class EncryptionResult:
    token: str


def encrypt_message(message: str, fernet_key: bytes) -> EncryptionResult:
    f = Fernet(fernet_key)
    token = f.encrypt(message.encode()).decode()
    return EncryptionResult(token=token)


def decrypt_message(token: str, fernet_key: bytes) -> str:
    f = Fernet(fernet_key)
    plaintext = f.decrypt(token.encode()).decode()
    return plaintext
