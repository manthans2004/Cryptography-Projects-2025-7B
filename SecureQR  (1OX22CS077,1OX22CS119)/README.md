# Secure QR

>Encrypted QR Code for Confidential Data Sharing

A cryptography project focused on securely sharing sensitive data using encrypted QR codes.

## Team Members
- K Madhu (1OX22CS077)
- Nithyashree H J (1OX22CS099)

## Project Overview
QR codes are widely used for data sharing but are inherently insecure for confidential information. This project, "SecureQR," provides a solution by integrating encryption with QR codes, ensuring that only authorized users can decode the data. Key features include:

1. **RSA Encryption:** Encrypt sensitive text or files before generating a QR code.
2. **QR Code Generation:** Encodes encrypted data as a QR code.
3. **Secure Decryption:** Authorized users can scan and decrypt the QR code to retrieve the original data.
4. **File Support:** Encrypt and share text, PDFs, or images via QR codes.

## Enhanced Features
- Generate QR codes for encrypted text or files
- Decrypt QR codes with proper keys
- Secure key management using RSA key pairs
- User-friendly web interface for generating and scanning QR codes
- Optional download of QR code images for sharing

## Objectives
- Ensure secure sharing of confidential information using QR codes
- Integrate asymmetric encryption (RSA) for strong security
- Support multiple file types for real-world applications
- Provide a simple, functional web interface for users
- Demonstrate the encryption/decryption process for educational purposes

## Installation & Usage

### Local Development
1. Clone the repository
```bash
git clone https://github.com/your-username/SecureQR.git
cd SecureQR

2. Install dependencies
bash
Copy code
pip install -r requirements.txt

3. Run the application
bash
Copy code
python app.py

4. Open your browser and navigate to http://localhost:5000

## Algorithm Details
The SecureQR workflow includes:
RSA Encryption: Encrypts sensitive data with a public key before encoding it as a QR code
QR Code Generation: Converts encrypted data into a scannable QR code
Decryption: Users with the private key can decode the QR code to retrieve the original data
File Handling: Supports text, PDF, and image file encryption
Optional Visualization: Displays the QR code for easy sharing

## Current Status
🚀 Deployment Ready – The application is functional and ready for practical use.


## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed for academic use as part of our university cryptography course.