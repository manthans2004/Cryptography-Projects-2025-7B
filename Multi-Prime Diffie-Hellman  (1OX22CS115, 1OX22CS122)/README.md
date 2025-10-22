# Multi-Prime Diffie-Hellman (MPDH) Key Exchange

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://github.com/Lyynn777/multi-prime-dh/blob/main/multi-prime-dh.ipynb)

Team Members: Nidhi Mannopantar (1OX22CS115), Pragya M S (1OX22CS122)
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
   - Interactive demo (TBA)

---

## **Performance Comparison**
- Benchmarks execution time for **multi-prime** vs **single-prime** DH.
- Visualized as a **bar chart** for easier analysis.

---

