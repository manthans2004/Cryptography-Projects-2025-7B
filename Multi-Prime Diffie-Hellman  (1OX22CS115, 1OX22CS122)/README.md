# Multi-Prime Diffie-Hellman (MPDH) Key Exchange

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://github.com/Lyynn777/multi-prime-dh/blob/main/multi-prime-dh.ipynb)

---

## **Project Overview**
This project demonstrates a **Multi-Prime Diffie-Hellman key exchange protocol**, where multiple primes are used instead of a single prime, allowing faster computation and secure key generation. The final shared key can be used for **symmetric encryption**, such as AES.

---

## **Features**
- Generate cryptographically secure primes.
- Compute private and public keys for Alice and Bob.
- Compute shared secret keys using multiple primes.
- Compare performance: **Multi-Prime vs Single-Prime DH**.
- Simulate network key exchange.
- Encrypt and decrypt messages using AES.
- Visual flowchart of the protocol.
- Interactive demo in Colab for experimenting with different number of primes and messages.

---

## **Getting Started**

### **Prerequisites**
- Python 3.x
- Libraries: `sympy`, `secrets`, `hashlib`, `matplotlib`, `pycryptodome`, `graphviz`, `ipywidgets`
- (All dependencies are installed in the notebook via `!pip install`)

### **Run the Notebook**
1. Open the notebook in **Google Colab** using the badge above.
2. Run each cell step by step.
3. Explore:
   - Prime generation
   - Key generation for Alice & Bob
   - Shared key computation
   - AES message encryption/decryption
   - Performance comparison
   - Interactive demo

---

## **Folder Structure**
multi-prime-dh/
│

├── Multi-Prime_Diffie_Hellman.ipynb # Main Colab notebook

├── multi_prime_dh_flowchart.png # Flowchart image generated in notebook

└── README.md # Project documentation


---

## **Interactive Demo**
- Use the slider to select **number of primes** (2–15).
- Enter a **message** to encrypt.
- The notebook will display:
  - Final shared key
  - Encrypted message (hex)
  - Decrypted message
  - Whether keys match

---

## **Performance Comparison**
- Benchmarks execution time for **multi-prime** vs **single-prime** DH.
- Visualized as a **bar chart** for easier analysis.

---

## **License**
This project is **open-source**. Feel free to use, modify, and share for educational purposes.

