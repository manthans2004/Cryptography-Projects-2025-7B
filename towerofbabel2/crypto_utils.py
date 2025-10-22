from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Dict, List, Tuple
from base64 import b64encode

from cryptography.hazmat.primitives import hashes, serialization, padding
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


# -----------------------------
# Certificate Authority (ECDSA)
# -----------------------------

class CertificateAuthority:
    """
    A tiny in-memory CA that signs user public keys using ECDSA.
    """

    def __init__(self):
        self._private_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
        self.public_key = self._private_key.public_key()
        self._registry: Dict[str, Dict] = {}

    def sign_user_pubkey(self, username: str, public_key) -> Dict:
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        # Bind username in the signed content to avoid substitution across identities
        content = b"USER:" + username.encode() + b"|PUB:" + pub_bytes
        signature = self._private_key.sign(content, ec.ECDSA(hashes.SHA256()))
        r, s = decode_dss_signature(signature)
        cert = {
            "username": username,
            "pub_der": pub_bytes,
            "sig_r": int(r),
            "sig_s": int(s),
        }
        self._registry[username] = cert
        return cert

    def verify_cert(self, cert: Dict) -> bool:
        username = cert["username"]
        pub_der = cert["pub_der"]
        r = cert["sig_r"]
        s = cert["sig_s"]
        content = b"USER:" + username.encode() + b"|PUB:" + pub_der
        signature = encode_dss_signature(r, s)
        try:
            self.public_key.verify(signature, content, ec.ECDSA(hashes.SHA256()))
            return True
        except Exception:
            return False


# -----------------------------
# Simulated user with ECC keypair
# -----------------------------

@dataclass
class SimulatedUser:
    name: str
    ca: CertificateAuthority

    def __post_init__(self):
        self.private_key = ec.generate_private_key(ec.SECP256R1(), backend=default_backend())
        self.public_key = self.private_key.public_key()
        self.certificate = self.ca.sign_user_pubkey(self.name, self.public_key)


# -----------------------------
# Helpers for serialization and cert verification
# -----------------------------

def serialize_public_key(public_key) -> str:
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pem.decode()


def verify_signed_public_key(ca: CertificateAuthority, user: SimulatedUser) -> None:
    # Verify the cert is valid and matches the user's current public key
    assert ca.verify_cert(user.certificate), "Invalid CA signature on user public key"
    # Check binding to actual key material
    current_der = user.public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    assert current_der == user.certificate["pub_der"], "Certificate does not match user's public key"


# -----------------------------
# ECDH shared secret and symmetric key derivation
# -----------------------------

def derive_symmetric_key(private_key, peer_public_key, context: bytes = b"") -> Tuple[bytes, Dict[str, str]]:
    """
    Derive a 256-bit symmetric key from ECDH shared secret using HKDF-like ConcatKDF with SHA-256.
    Context includes both public keys and optional caller-provided context to bind direction.
    Returns (key, debug_info)
    """
    shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)  # Raw ECDH secret

    # Construct context info to prevent key reuse/malleability across different pairs/directions
    self_pub = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    peer_pub = peer_public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    # Use a canonical order for the two public keys so both parties derive the same key
    p1, p2 = sorted([self_pub, peer_pub])
    info = b"CTX:" + context + b"|P1:" + p1 + b"|P2:" + p2

    ckdf = ConcatKDFHash(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key
        otherinfo=info,
        backend=default_backend(),
    )
    key = ckdf.derive(shared_secret)

    debug = {
        "shared_secret_hash_hex": hashlib.sha256(shared_secret).hexdigest(),
    }
    return key, debug


# -----------------------------
# AES-CBC with PKCS7 padding
# -----------------------------

def aes_cbc_encrypt(key: bytes, plaintext: bytes) -> Tuple[bytes, bytes]:
    # Random IV: derive via os.urandom
    import os

    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return iv, ciphertext


def aes_cbc_decrypt(key: bytes, iv: bytes, ciphertext: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()
    return plaintext


# -----------------------------
# Obfuscation layer: deterministic block permutation
# -----------------------------

def _split_blocks(data: bytes, block_size: int = 16) -> List[bytes]:
    assert len(data) % block_size == 0, "Ciphertext not aligned to block size"
    return [data[i : i + block_size] for i in range(0, len(data), block_size)]


def _join_blocks(blocks: List[bytes]) -> bytes:
    return b"".join(blocks)


def _deterministic_permutation(key: bytes, iv: bytes, n: int) -> List[int]:
    """
    Create a deterministic permutation of range(n) by sorting indices by SHA256(key||iv||i).
    This is not for security; it's a demonstrative obfuscation step.
    """
    scores = []
    for i in range(n):
        h = hashlib.sha256(key + iv + i.to_bytes(4, "big")).digest()
        scores.append((h, i))
    scores.sort(key=lambda t: t[0])
    return [i for _, i in scores]


def obfuscate_ciphertext_blocks(key: bytes, iv: bytes, ciphertext: bytes) -> Tuple[bytes, List[int]]:
    blocks = _split_blocks(ciphertext, 16)
    n = len(blocks)
    perm = _deterministic_permutation(key, iv, n)
    permuted_blocks = [blocks[i] for i in perm]
    return _join_blocks(permuted_blocks), perm


def deobfuscate_ciphertext_blocks(key: bytes, iv: bytes, permuted_ciphertext: bytes, perm: List[int]) -> bytes:
    obf_blocks = _split_blocks(permuted_ciphertext, 16)
    n = len(obf_blocks)
    assert n == len(perm), "Permutation mismatch"
    # Build inverse permutation
    inv = [0] * n
    for new_pos, src_idx in enumerate(perm):
        inv[src_idx] = new_pos
    # Reconstruct original order
    orig_blocks = [None] * n
    for orig_index in range(n):
        orig_blocks[orig_index] = obf_blocks[inv[orig_index]]
    return _join_blocks(orig_blocks)
