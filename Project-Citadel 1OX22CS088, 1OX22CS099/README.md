
# Project Citadel

> Reinforcing the Hill Cipher with Non-Linear Diffusion and CBC Mode

A  cryptography project focused on analyzing the classical Hill Cipher and designing a modern, more secure enhancement.

## Team Members
- Manthan S(1OX22CS099)
- Likhith U(1OX22CS088)

## Project Overview
The classical Hill Cipher, while innovative for its use of matrix algebra, suffers from critical vulnerabilities like linearity and susceptibility to known-plaintext attacks. This project, "Project Citadel," aims to reinforce it by integrating:
1.  **Non-Linear Diffusion:** Using a custom S-Box to break the linear relationship.
2.  **CBC Mode:** Implementing Cipher Block Chaining to hide patterns in the plaintext.
3.  **File Encryption:** Extending the cipher to support PDF and image encryption.

## Enhanced Features
- Text encryption/decryption with step-by-step visualization
- PDF file encryption/decryption capabilities
- Image file encryption/decryption capabilities
- Modern web interface for easy interaction
- Secure key management with IV values

## Objectives
- Analyze the mathematical structure and weaknesses of the original Hill Cipher.
- Design a new algorithm incorporating non-linear components.
- Demonstrate the enhanced security through a manual worked example.
- Provide a functional implementation for text and file encryption.
- Deploy a web application for practical use.

## Installation & Usage

### Local Development
1. Clone the repository
```bash
git clone https://github.com/manthans2004/Project-Citadel.git
cd Project-Citadel
```

2. Checkout the deployment branch
```bash
git checkout final_citadel_deployment
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the application
```bash
python app.py
```

5. Open your browser and navigate to `http://localhost:5000`

### Deployment
The application is configured for deployment on Heroku or similar platforms. The main deployment branch is `final_citadel_deployment`.

## Algorithm Details
The enhanced Hill Cipher in Project Citadel includes:
- Matrix-based encryption with modular arithmetic (mod 256 for binary data)
- Custom S-Box: S(x) = (7x + 3) mod 26 for text, modified for binary operations
- Cipher Block Chaining (CBC) mode for better security
- Support for both text and binary file encryption

## Current Status
🚀 **Deployment Ready** - The application is complete and ready for deployment on the `final_citadel_deployment` branch.



## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed for academic use as part of our university cryptography course.
```
