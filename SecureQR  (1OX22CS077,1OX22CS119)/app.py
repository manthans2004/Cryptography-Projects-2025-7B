from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import qrcode, io, base64
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import cv2
import numpy as np

app = Flask(__name__)
app.secret_key = "dev-secret"  # only for demo

# Generate RSA keys once at startup (temporary for this run)
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Save private key to file so user can download it (special key)
with open("private_key.pem", "wb") as f:
    f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

with open("public_key.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    message = request.form.get('message', '').encode('utf-8')
    if not message:
        flash("Please provide a message to encrypt.")
        return redirect(url_for('index'))

    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

    # create QR with hex representation
    qr = qrcode.QRCode(version=1, box_size=6, border=4)
    qr.add_data(ciphertext.hex())
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # convert PIL image to base64 for embedding
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    img_b64 = base64.b64encode(buf.read()).decode('ascii')

    return render_template('encrypt_result.html', qr_base64=img_b64)


@app.route('/download_private')
def download_private():
    # Provide the private key to the user to keep (special key).
    return send_file("private_key.pem", as_attachment=True)


@app.route('/decrypt', methods=['POST'])
def decrypt():
    qr_file = request.files.get('qr_file')
    key_file = request.files.get('key_file')

    if not qr_file or not key_file:
        flash("Please upload both a QR image and the private key file (.pem).")
        return redirect(url_for('index'))

    # read private key
    key_bytes = key_file.read()
    try:
        private = load_pem_private_key(key_bytes, password=None)
    except Exception as e:
        flash(f"Failed to load private key: {e}")
        return redirect(url_for('index'))

    # read QR image bytes into numpy array for OpenCV
    file_bytes = np.frombuffer(qr_file.read(), np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if not data:
        flash("No QR code detected in the uploaded image.")
        return redirect(url_for('index'))

    try:
        ciphertext = bytes.fromhex(data)
        plaintext = private.decrypt(
            ciphertext,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        message = plaintext.decode('utf-8')
    except Exception as e:
        flash(f"Decryption failed: {e}")
        return redirect(url_for('index'))

    return render_template('decrypt_result.html', message=message)


if __name__ == '__main__':
    # Run on all interfaces for convenience; change as needed for security.
    app.run(host='0.0.0.0', port=5000, debug=True)
