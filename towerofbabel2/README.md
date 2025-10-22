# Tower of Babel - ECC Hybrid Cryptography Demo (Flask)

A minimal, educational Flask web app demonstrating a hybrid cryptography pipeline:

- ECC key generation (P-256) per user
- Authenticated key exchange via a tiny ECDSA-based Certificate Authority (CA)
- ECDH shared secret -> SHA-256 based KDF -> AES-256-CBC encryption
- Obfuscation layer ("Tower of Babel"): deterministic permutation of ciphertext blocks

This app is for learning and demos only; not production hardened.

Link to check it out:
https://towerofbabel.onrender.com/

## Prerequisites

- Python 3.10+
- pip

## Setup

```bash
# In a terminal, from the project directory
python -m venv .venv
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

## Run

```bash
# From the project directory
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## How it works

- On startup, a mini `CertificateAuthority` is created along with three users: Alice, Bob, Carol.
- The CA ECDSA-signs each user's public key (binding username and key bytes).
- When you submit a message:
  - The sender verifies both their own and the recipient's CA-signed public keys.
  - The sender derives a symmetric key from the ECDH shared secret using `ConcatKDFHash(SHA-256)` with context binding (`sender->recipient`, plus both public keys).
  - The message is encrypted with AES-CBC and PKCS#7 padding.
  - Ciphertext blocks are then permuted deterministically using SHA-256(key||iv||i) as a score for index `i`.
  - The recipient reproduces the same derived key, de-permutes the blocks, and decrypts the message.

## Notes

- This demo intentionally shows internals like public keys, a hash of the ECDH shared secret, the IV, and the permutation list to aid understanding.
- The obfuscation is not a replacement for authenticated encryption. For robust security, use an AEAD mode (e.g., AES-GCM) and proper certificate/PKI.

## Structure

- `app.py` - Flask app and routes
- `crypto_utils.py` - ECC, CA, ECDH, KDF, AES-CBC, obfuscation
- `templates/index.html` - UI template

## License

MIT
