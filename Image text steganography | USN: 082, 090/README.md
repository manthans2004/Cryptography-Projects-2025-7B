# 🖼️ Image Text Steganography Project

This project demonstrates **Image Text Steganography** — the technique of hiding secret text messages inside an image.  
The message is embedded in the pixel data of the image (using the Least Significant Bit technique), making it invisible to the human eye.  

---

## 🚀 Features
- Hide (embed) a secret message inside an image.
- Extract (recover) the hidden message.
- Optional AES encryption for better security (Python version).
- Simple web-based demo (HTML version) — no installation needed.
- Beautiful user interface with colorful design.

---

## 🧰 Tools & Libraries Used
### Python Version
- **Python 3.12**
- **Pillow (PIL)** → Image processing  
- **NumPy** → Pixel-level operations  
- **PyCryptodome** → AES encryption/decryption  

### Web Version
- **HTML, CSS, JavaScript**  
- Uses HTML `<canvas>` API for pixel manipulation.

---

## 🧩 Working Principle
1. Convert the message into binary form (sequence of 0s and 1s).  
2. Embed these bits into the **Least Significant Bits (LSB)** of image pixels.  
3. Save the modified image as the **stego image**.  
4. During extraction, read these LSBs and reconstruct the original message.  

---

## 🐍 Python Implementation

### 🔹 To Embed and Extract Message
```python
from PIL import Image
import numpy as np
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import os

cover_path = r"C:\Users\Admin\Desktop\cover.png"
stego_path = r"C:\Users\Admin\Desktop\stego.png"

embed_text_into_image(cover_path, stego_path, "Hello Keerthana!", password="mypassword")
secret = extract_text_from_image(stego_path, password="mypassword")
print("Recovered message:", secret)
```

### ✅ Example Output
```
[+] Embedded message (40 bytes) into C:\Users\Admin\Desktop\stego.png
Recovered message: Hello Keerthana!
```

---

## 🌐 HTML Version (No Python Required)

- Open the **HTML file** in your browser.  
- Upload a cover image (`.png` or `.jpg`).  
- Type your secret message.  
- Click **"Embed & Download"** to save the stego image.  
- Later, upload that stego image and click **"Extract Message"** to reveal the text.

### 🎨 Colorful UI Screenshot
*(You can insert a screenshot of your webpage here)*

---

## 🧠 Explanation of Output
- The console or webpage shows:
  ```
  Recovered Message: Hello Keerthana!
  ```
  This means the hidden message has been successfully extracted from the image.

- The stego image looks exactly the same as the original to the human eye, but internally it contains the secret text.

---

## ⚙️ Common Errors & Fixes
| Issue | Cause | Fix |
|-------|--------|-----|
| `FileNotFoundError` | Wrong image path | Provide full image path (e.g., `C:\Users\Admin\Desktop\cover.png`) |
| `ModuleNotFoundError: No module named 'Crypto'` | Missing PyCryptodome | Run `pip install pycryptodome` |
| Gibberish Output (in web version) | Encrypted data read as plain text | Use simple message without encryption |

---

## 🏁 Conclusion
This project successfully hides and retrieves secret messages from images using steganography.  
It showcases basic cryptography, image processing, and web technologies in a single mini-project — perfect for academic presentation or GitHub portfolio.

---

## 👩‍💻 Developed by
**Keerthana C N**  
B.Tech in Computer Science and Engineering  
The Oxford College of Engineering, Bengaluru
