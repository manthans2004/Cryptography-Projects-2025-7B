from flask import Flask, render_template, request
from base64 import b64encode, b64decode
from typing import Dict, Tuple

from crypto_utils import (
    CertificateAuthority,
    SimulatedUser,
    derive_symmetric_key,
    aes_cbc_encrypt,
    aes_cbc_decrypt,
    obfuscate_ciphertext_blocks,
    deobfuscate_ciphertext_blocks,
    serialize_public_key,
    verify_signed_public_key,
)

app = Flask(__name__)

# Initialize a simple CA and a few users (Alice, Bob, Carol)
CA = CertificateAuthority()
USERS: Dict[str, SimulatedUser] = {
    name: SimulatedUser(name=name, ca=CA) for name in ["Alice", "Bob", "Carol"]
}


def perform_ecdh_and_encrypt(sender: SimulatedUser, recipient: SimulatedUser, message: str):
    # Verify both parties' certs before using their keys
    verify_signed_public_key(CA, sender)
    verify_signed_public_key(CA, recipient)

    # Derive a shared key using ECDH (sender's private, recipient's public)
    context = f"{sender.name}->{recipient.name}".encode()
    shared_key, debug = derive_symmetric_key(sender.private_key, recipient.public_key, context=context)

    # Encrypt using AES-CBC and then obfuscate the ciphertext blocks
    iv, ciphertext = aes_cbc_encrypt(shared_key, message.encode("utf-8"))
    permuted_ct, permutation = obfuscate_ciphertext_blocks(shared_key, iv, ciphertext)

    # For demo, also try to decrypt back as the recipient
    # Recipient derives the same key using their private key and sender's public key
    shared_key_r, _ = derive_symmetric_key(recipient.private_key, sender.public_key, context=context)
    # Deobfuscate then decrypt
    restored_ct = deobfuscate_ciphertext_blocks(shared_key_r, iv, permuted_ct, permutation)
    plaintext = aes_cbc_decrypt(shared_key_r, iv, restored_ct).decode("utf-8", errors="replace")

    # Prepare display items
    display = {
        "sender": sender.name,
        "recipient": recipient.name,
        "sender_pub": serialize_public_key(sender.public_key),
        "recipient_pub": serialize_public_key(recipient.public_key),
        "ca_pub": serialize_public_key(CA.public_key),
        "shared_secret_hash_hex": debug["shared_secret_hash_hex"],
        "context": context.decode(),
        "iv_b64": b64encode(iv).decode(),
        "ciphertext_b64": b64encode(ciphertext).decode(),
        "permuted_ciphertext_b64": b64encode(permuted_ct).decode(),
        "permutation": permutation,
        "decrypted_plaintext": plaintext,
    }
    return display


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    message = ""
    sender = "Alice"
    recipient = "Bob"

    if request.method == "POST":
        message = request.form.get("message", "")
        sender = request.form.get("sender", "Alice")
        recipient = request.form.get("recipient", "Bob")
        if not message:
            error = "Please enter a message to encrypt."
        elif sender not in USERS or recipient not in USERS:
            error = "Invalid sender or recipient."
        else:
            try:
                result = perform_ecdh_and_encrypt(USERS[sender], USERS[recipient], message)
            except Exception as e:
                error = f"Error: {e}"

    user_names = list(USERS.keys())
    return render_template(
        "index.html",
        users=user_names,
        result=result,
        error=error,
        message=message,
        selected_sender=sender,
        selected_recipient=recipient,
    )


if __name__ == "__main__":
    # Run the Flask app
    app.run(debug=True)
