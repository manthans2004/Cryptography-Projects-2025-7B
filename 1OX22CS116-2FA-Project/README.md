# MLS-2FA: Two-Factor Authentication Project

## Team Members
- Nikhil NV (USN: 1OX22CS116)

## Project Description
This project is a Proof of Concept (PoC) for a Two-Factor Authentication (2FA) system using cryptography and steganography. Users register by selecting a secret image, clicking a secret spot, and setting a passphrase. Authentication requires the correct image, spot, and passphrase, making the system highly secure.

## Features
- User registration with image, secret spot, and passphrase
- Secure token encryption using Fernet (cryptography)
- Steganography for hiding tokens in images
- Decoy images for added security
- Admin debug tools for ciphertext inspection

## Steps to Run the Project

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
2. Run the application:
   ```
python main.py
   ```

do it in virtual environment


