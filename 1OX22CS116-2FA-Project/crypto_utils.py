from __future__ import annotations

import base64
import hashlib
from typing import Tuple

from cryptography.fernet import Fernet, InvalidToken


def derive_fernet_key_from_passphrase(passphrase: str, salt: str = "mls-2fa-poc") -> bytes:
	"""Derive a Fernet key from a passphrase using SHA256 + urlsafe_b64.
	This is a simple PoC derivation, not recommended for production.
	"""
	hash_bytes = hashlib.sha256((passphrase + salt).encode("utf-8")).digest()
	return base64.urlsafe_b64encode(hash_bytes)


def encrypt_token_with_passphrase(token: str, passphrase: str) -> bytes:
	key = derive_fernet_key_from_passphrase(passphrase)
	fernet = Fernet(key)
	return fernet.encrypt(token.encode("utf-8"))


def decrypt_token_with_passphrase(ciphertext: bytes, passphrase: str) -> Tuple[bool, str | None]:
	key = derive_fernet_key_from_passphrase(passphrase)
	fernet = Fernet(key)
	try:
		plaintext = fernet.decrypt(ciphertext)
		return True, plaintext.decode("utf-8")
	except InvalidToken:
		return False, None