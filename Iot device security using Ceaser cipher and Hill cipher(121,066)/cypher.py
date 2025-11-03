import numpy as np
import tkinter as tk
from tkinter import messagebox

# ---------------- CAESAR CIPHER ----------------
def caesar_encrypt(text, shift):
    result = ""
    for char in text.upper():
        if char.isalpha():
            result += chr((ord(char) - 65 + shift) % 26 + 65)
        else:
            result += char
    return result

def caesar_decrypt(cipher, shift):
    return caesar_encrypt(cipher, -shift)

# ---------------- HILL CIPHER ----------------
def hill_encrypt(text, key_matrix):
    numbers = [ord(c) - 65 for c in text.upper()]
    n = key_matrix.shape[0]
    while len(numbers) % n != 0:
        numbers.append(25)  # padding with Z
    
    cipher_nums = []
    for i in range(0, len(numbers), n):
        block = np.array(numbers[i:i+n]).reshape(n, 1)
        encrypted_block = np.dot(key_matrix, block) % 26
        cipher_nums.extend(encrypted_block.flatten())
    
    return ''.join(chr(num + 65) for num in cipher_nums)

def hill_decrypt(cipher, key_matrix):
    n = key_matrix.shape[0]
    numbers = [ord(c) - 65 for c in cipher.upper()]

    det = int(np.round(np.linalg.det(key_matrix)))
    det_inv = pow(det, -1, 26)  # modular inverse
    matrix_mod_inv = (
        det_inv * np.round(det * np.linalg.inv(key_matrix)).astype(int)
    ) % 26
    
    plain_nums = []
    for i in range(0, len(numbers), n):
        block = np.array(numbers[i:i+n]).reshape(n, 1)
        decrypted_block = np.dot(matrix_mod_inv, block) % 26
        plain_nums.extend(decrypted_block.flatten())
    
    return ''.join(chr(num + 65) for num in plain_nums)

# ---------------- HYBRID FUNCTIONS ----------------
def hybrid_encrypt(message, shift, key_matrix):
    caesar_out = caesar_encrypt(message, shift)
    hill_out = hill_encrypt(caesar_out, key_matrix)
    return caesar_out, hill_out

def hybrid_decrypt(cipher, shift, key_matrix):
    hill_out = hill_decrypt(cipher, key_matrix)   # reverse Hill
    original = caesar_decrypt(hill_out, shift)    # reverse Caesar
    return hill_out, original

# ---------------- GUI APP ----------------
def process_data(mode):
    message = entry_message.get().strip()
    shift = entry_shift.get().strip()

    if not message or not shift.isdigit():
        messagebox.showerror("Error", "Please enter valid text and shift value!")
        return

    shift = int(shift)
    key_matrix = np.array([[3, 3], [2, 5]])  # invertible Hill key

    if mode == "E":  # Encrypt
        caesar_out, hybrid_out = hybrid_encrypt(message, shift, key_matrix)
        result.set(f"[ENCRYPTION]\nCaesar Output: {caesar_out}\nHybrid Output: {hybrid_out}")

    elif mode == "D":  # Decrypt (user enters Hybrid output!)
        hill_out, original = hybrid_decrypt(message, shift, key_matrix)
        result.set(f"[DECRYPTION]\nAfter Hill Decrypt: {hill_out}\nRecovered Plaintext: {original}")

# ---------------- MAIN WINDOW ----------------
root = tk.Tk()
root.title("IoT Data Security - Caesar + Hill Cipher")
root.geometry("520x320")
root.config(bg="#f0f0f0")

# Input fields
tk.Label(root, text="Enter Text (Plaintext for Encryption / Hybrid Output for Decryption):", bg="#f0f0f0").pack(pady=5)
entry_message = tk.Entry(root, width=50)
entry_message.pack()

tk.Label(root, text="Enter Caesar Shift (1-25):", bg="#f0f0f0").pack(pady=5)
entry_shift = tk.Entry(root, width=10)
entry_shift.pack()

# Buttons
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

btn_encrypt = tk.Button(frame, text="Encrypt", command=lambda: process_data("E"), bg="#4CAF50", fg="white")
btn_encrypt.grid(row=0, column=0, padx=10)

btn_decrypt = tk.Button(frame, text="Decrypt", command=lambda: process_data("D"), bg="#f44336", fg="white")
btn_decrypt.grid(row=0, column=1, padx=10)

# Result area
result = tk.StringVar()
lbl_result = tk.Label(root, textvariable=result, bg="#e6e6e6", width=65, height=7, anchor="nw", justify="left")
lbl_result.pack(pady=10)

root.mainloop()
