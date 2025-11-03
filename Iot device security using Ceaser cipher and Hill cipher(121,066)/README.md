# 🔐 IoT Data Security using Caesar Cipher and Hill Cipher

## 📘 Overview
With the rapid growth of the **Internet of Things (IoT)**, billions of devices now communicate and share sensitive data. However, many IoT systems lack adequate encryption because traditional algorithms like AES and RSA are too computationally heavy for small, low-power devices.

This project presents a **lightweight hybrid encryption model** that combines the **Caesar Cipher** and **Hill Cipher** to secure IoT data efficiently. The approach provides a balance between **security, simplicity, and performance**, making it suitable for **resource-constrained IoT environments**.

---

## 🎯 Objectives
1. **Analyze** the weaknesses of classical Caesar and Hill ciphers.  
2. **Design** a hybrid encryption algorithm that improves data confidentiality.  
3. **Implement** both encryption and decryption in Python using modular arithmetic.  
4. **Demonstrate** lightweight encryption suitable for IoT sensor data.  
5. **Test** the model for speed, accuracy, and reversibility (perfect decryption).

---

## ⚙️ Algorithm Flow

### **Encryption**
1. The user enters plaintext and two keys — a **shift key** (for Caesar Cipher) and a **key matrix** (for Hill Cipher).  
2. The plaintext is first processed using the **Caesar Cipher**, shifting each character by the shift key value.  
3. The result is then passed to the **Hill Cipher**, where the data is divided into blocks and multiplied by the key matrix (mod 26).  
4. The output is the **final ciphertext**, suitable for secure transmission between IoT devices.

### **Decryption**
1. The ciphertext is first processed using the **Inverse Hill Cipher**, multiplying with the inverse key matrix (mod 26).  
2. The resulting text is then passed through the **reverse Caesar Cipher**, shifting characters backward using the same shift key.  
3. The output is the **original plaintext**, recovered successfully.

---

## 🧠 Technologies Used
### **Programming Language**
- **Python** — Core language for encryption, decryption, and matrix computations.

### **Python Libraries**
- **NumPy** — For matrix multiplication and modular arithmetic.  
- **sys / math** — For handling input, validation, and modular inverse operations.  

### **Tools**
- **VS Code / IDLE / Jupyter Notebook** — Used for writing and testing the program.  
- **Command Line Interface (CLI)** — To run and test encryption/decryption.  

---

## 🧩 System Architecture
User Input (Plaintext + Keys)
↓
Caesar Cipher (Shift)
↓
Hill Cipher (Matrix Multiplication Mod 26)
↓
Ciphertext (Output)
↓
Decryption (Inverse Process)
↓
Recovered Plaintext


🧪 Features

✅ Hybrid encryption using two classical ciphers (Caesar + Hill).

✅ Lightweight and fast — ideal for IoT devices with limited resources.

✅ Fully reversible — lossless decryption of original data.

✅ Simple to implement and extend with modern cipher layers.

✅ Educational and practical — demonstrates cryptography fundamentals.

💡 Future Enhancements

🔹 Integrate key generation based on device IDs or timestamps for dynamic encryption.

🔹 Extend support from mod 26 → mod 256 to handle binary files and sensor data streams.

🔹 Add a graphical interface (GUI) for non-technical users.

🔹 Implement S-Box transformation to introduce non-linearity and resist linear attacks.

🔹 Enable network-level encryption for IoT device communication.

👨‍💻 Contributors

Harshitha V M(1OX22CS066)
Pooja M(1OX22CS121)

🏁 Conclusion

This project successfully demonstrates how combining Caesar Cipher and Hill Cipher can enhance IoT data security without overloading limited hardware. The hybrid approach ensures faster execution, stronger encryption than either cipher alone, and adaptability for future IoT encryption frameworks.

