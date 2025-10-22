CIPHER CASCADE: MULTI-LAYER DATA PROTECTION

Team Members:
 
 Nandini B - 1OX22CS109
 Lavanya - 1OX22CS087

Short Description:

Our project implements a multi-layer hybrid encryption system that enhances the security of plaintext messages using a combination of classical cryptographic techniques — the Hill Cipher, Caesar Cipher, and One-Time Pad (OTP).

It allows users to input any plaintext along with their chosen encryption keys and automatically encrypts and decrypts messages while preserving spaces, punctuation, and letter casing for readability and exact recovery.
The system first uses the Hill cipher to transform text into encrypted blocks using matrix multiplication over modular arithmetic, introducing a strong algebraic mixing of characters. Next, the Caesar cipher adds a secondary layer of security by shifting each letter by a user-defined amount. Finally, an OTP (One-Time Pad) applies a unique numerical sequence to each character, making the ciphertext resistant to frequency analysis and brute-force attacks. During decryption, all steps are precisely reversed — ensuring the original plaintext is fully recovered without loss.

Steps to Run:

1.	Open eclipse, create a project – project name (cnspro)
2.	For class – create in cnspro package only 
3.	And create a file with .java extension (hybrid.java) and paste our code and save it.
4.	Run and give your input with plaintext, keys and others.
5.	Then it will give encrypted and decrypted output.

Screenshots:

Plaintext and Key Inputs:CNS1.jpg
Encrypted Output: cns2.jpg
Decrypted Output: cns3.jpg

 


  

