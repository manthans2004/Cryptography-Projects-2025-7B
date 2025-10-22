# 🔐 Hybrid Caesar–Vigenère Cipher (Advanced Web Implementation)

## 👥 Team Members
| Name | USN |
|------|-----|
| Kirthi Keshav Madival | [1OX22CS086] |
| [J N Varshitha] | [1OX22CS072] |

---

## 🧠 Project Description
This project implements a **Hybrid Caesar–Vigenère Cipher**, a classical cryptography concept that combines two famous substitution techniques — **Caesar Cipher** and **Vigenère Cipher** — to create a stronger, layered encryption mechanism.

### ✨ How It Works
1. **Caesar Cipher Stage** – Shifts each plaintext letter by a fixed numeric key (`k`).
2. **Vigenère Cipher Stage** – Encrypts the Caesar output again using a repeating keyword.
3. **Decryption** reverses the process: first Vigenère, then Caesar.

This combination makes the cipher more secure against frequency and brute-force attacks while remaining lightweight and easy to understand.

---

## 🚀 Steps to Run the Project

1. **Download or Clone the Repository**
   ```bash
   git clone https://github.com/your-username/hybrid-caesar-vigenere.git
   ```
   *(Or simply copy the HTML file to your local system.)*

2. **Open the Project**
   - Locate the file: `index.html`
   - Double-click it or right-click → **Open with Browser**

3. **Use the Interface**
   - Enter your **plaintext**
   - Choose a **Caesar Shift** (any number between 0–25)
   - Enter a **Vigenère Key** (any alphabetic keyword)
   - Click **Encrypt & Decrypt**
   - View results for:
     - Caesar step output
     - Vigenère encryption
     - Final encrypted text
     - Decrypted text verification

---

## 🧩 Example

**Plaintext:** HELLO  
**Caesar Shift:** 3  
**Vigenère Key:** KEY  

**Process:**
1. After Caesar → KHOOR  
2. After Vigenère → ULMYV  
3. After Decryption → HELLO ✅

---


## ⚙️ Tech Stack
- **HTML5** – Structure  
- **CSS3** – Styling & UI design  
- **JavaScript (Vanilla JS)** – Cipher logic and functionality  

---

## 📘 Educational Purpose
This project is designed for academic demonstration to explain:
- Classical cryptography techniques  
- Layered encryption  
- Simple web-based implementation of ciphers  

---

## 🏁 Conclusion
The **Hybrid Caesar–Vigenère Cipher** improves upon traditional Caesar and Vigenère techniques by combining both into a single two-step process.  
It demonstrates how layering simple encryption methods can enhance security and understanding of cryptographic principles.
