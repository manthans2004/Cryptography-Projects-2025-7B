from flask import Blueprint, jsonify, render_template, request

from .crypto_utils import (
    compute_public_key,
    compute_shared_secret,
    derive_symmetric_key,
    encrypt_message,
    decrypt_message,
)

bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("index.html")


@bp.post("/api/compute")
def compute():
    data = request.get_json(force=True)
    try:
        p = int(data.get("p"))
        g = int(data.get("g"))
        a = int(data.get("a"))
        b = int(data.get("b"))
    except Exception:
        return jsonify({"error": "Invalid inputs. p, g, a, b must be integers."}), 400

    if not (p and g and a and b):
        return jsonify({"error": "Missing one or more required fields: p, g, a, b."}), 400

    # Compute public keys
    A = compute_public_key(g, a, p)
    B = compute_public_key(g, b, p)

    # Compute shared secrets (both should match)
    s1 = compute_shared_secret(B, a, p)
    s2 = compute_shared_secret(A, b, p)

    return jsonify({
        "A": A,
        "B": B,
        "s1": s1,
        "s2": s2,
        "match": s1 == s2,
    })


@bp.post("/api/encrypt")
def api_encrypt():
    data = request.get_json(force=True)
    try:
        p = int(data.get("p"))
        g = int(data.get("g"))
        a = int(data.get("a"))
        b = int(data.get("b"))
        sender = data.get("sender")  # 'alice' or 'bob'
        message = data.get("message", "")
    except Exception:
        return jsonify({"error": "Invalid inputs."}), 400

    if sender not in ("alice", "bob"):
        return jsonify({"error": "sender must be 'alice' or 'bob'"}), 400

    # Compute public keys
    A = compute_public_key(g, a, p)
    B = compute_public_key(g, b, p)

    # Sender uses recipient's public key with their private key to compute the shared secret
    if sender == "alice":
        shared = compute_shared_secret(B, a, p)
    else:
        shared = compute_shared_secret(A, b, p)

    fkey = derive_symmetric_key(shared, p, g)
    enc = encrypt_message(message, fkey)

    return jsonify({
        "ciphertext": enc.token,
        "shared_secret": shared,  # shown for demo transparency; do not do this in real apps
    })


@bp.post("/api/decrypt")
def api_decrypt():
    data = request.get_json(force=True)
    try:
        p = int(data.get("p"))
        g = int(data.get("g"))
        a = int(data.get("a"))
        b = int(data.get("b"))
        recipient = data.get("recipient")  # 'alice' or 'bob'
        ciphertext = data.get("ciphertext", "")
    except Exception:
        return jsonify({"error": "Invalid inputs."}), 400

    if recipient not in ("alice", "bob"):
        return jsonify({"error": "recipient must be 'alice' or 'bob'"}), 400

    A = compute_public_key(g, a, p)
    B = compute_public_key(g, b, p)

    # Recipient derives the same shared secret
    if recipient == "alice":
        shared = compute_shared_secret(B, a, p)
    else:
        shared = compute_shared_secret(A, b, p)

    fkey = derive_symmetric_key(shared, p, g)
    try:
        plaintext = decrypt_message(ciphertext, fkey)
    except Exception:
        return jsonify({"error": "Decryption failed. Check keys and ciphertext."}), 400

    return jsonify({
        "plaintext": plaintext,
        "shared_secret": shared,
    })
