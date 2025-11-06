# Crack-Time-Estimator

### Team Members
-Maidin Sayed-1OX22CS094
-Imthiyaz K-1OX22CS071

### Project Description
“Crack Time Estimator” is a web-based cryptography and cybersecurity project designed to estimate how long it would take to crack a given password through brute-force or dictionary attacks. The application serves as an educational and analytical tool, helping users understand the relationship between password complexity, entropy, and real-world security.

Built using Python (Flask) for backend computation and HTML, CSS, and JavaScript for the frontend visualization, the system evaluates password strength based on parameters such as length, character diversity, and pattern predictability. It then calculates the entropy of the password and estimates the time required to crack it under different attack speeds (e.g., offline brute force, online rate-limited attacks).

The project aims to bridge the gap between theoretical password security concepts and practical understanding through an interactive web interface that visualizes password strength and crack time in real-time. Users can enter any password and immediately see an estimated crack duration ranging from milliseconds to centuries, accompanied by a color-coded visual meter and security suggestions.

All processing is performed locally or via a lightweight backend service, ensuring user privacy by not storing or transmitting password data. The project highlights the importance of strong password creation and demonstrates how modern computing power affects password vulnerability.

Beyond its educational value, Crack Time Estimator serves as a cybersecurity awareness tool that encourages users to adopt better password hygiene. It also provides students a practical demonstration of cryptographic entropy, logarithmic scaling, and secure front-end design principles.

### Steps to Run the Project 
1. Open a terminal in this project folder
2. Install required dependencies:pip install-r requirements.txt
3. Run the application:python app.py
4. Open the browser and go to the link shown (usually http://127.0.0.1:5000).
5. Enter a password to check its estimated crack time.

### Screenshots

![Homepage](./screenshots/home.png)
![Result Page](./screenshots/result.png)

### Live Demo
https://crack-time-estimator.onrender.com

Application is live!!
