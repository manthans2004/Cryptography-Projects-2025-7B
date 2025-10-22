What is "Odd-Even Split & Mix"? 
• It's a two-part hybrid cipher for encrypting messages. 
• It splits the plaintext message into two separate sequences based on the position of 
each letter: odd positions and even positions. 
• The odd-positioned letters are encrypted using a Playfair cipher. 
• The even-positioned letters are taken in reverse order and encrypted using a 
monoalphabetic substitution cipher. 
• The final ciphertext is created by concatenating the two encrypted parts.
Rules
 1. Number letters left→right starting at 1.
 2. Odd letters = positions 1,3,5,... — we keep their left→right order. Encrypt these with Playfair.
 3. Even letters = positions 2,4,6,... — take them but reverse their order (take from the back). 
Encrypt those with monoalphabetic substitution.
 4. Final ciphertext = Playfair-output (odds) + Mono-output (evens).
 5. To decrypt: split back using counts, decrypt each part, reverse the even sequence back, then re
insert odds and evens into original positions.
Encryption Pseudocode
 Algorithm Encrypt_SplitMix(P, K1, K2)
 Input:
   P   → Plaintext
   K1  → Playfair key
   K2  → Monoalphabetic substitution key
 Output:
   C   → Ciphertext
 
Begin
   1. Preprocess P
       a. Remove spaces, convert to uppercase
       b. Replace J with I
       c. If length(P) is odd, append filler 'X'
 
   2. Split P into odd and even sequences
       P_odd  ← letters at positions 1,3,5,...
       P_even ← letters at positions 2,4,6,... (then reverse order)
 
   3. Encrypt odd part using Playfair
       C_odd ← Playfair_Encrypt(P_odd, K1)
 
   4. Encrypt even part using Monoalphabetic substitution
       C_even ← Mono_Encrypt(P_even, K2)
 
   5. Concatenate results
       C ← C_odd || C_even
 
   Return C
 End
Decryption Pseudocode
 Algorithm Decrypt_SplitMix(C, K1, K2, n)
 Input:
   C   → Ciphertext
   K1  → Playfair key
   K2  → Monoalphabetic substitution key
   n   → Original plaintext length
 Output:
   P   → Plaintext
 
Begin
   1. Split C into two parts
       odd_count ← ceil(n/2)
       C_odd  ← first odd_count characters
       C_even ← remaining characters
 
   2. Decrypt odd part using Playfair
       P_odd ← Playfair_Decrypt(C_odd, K1)
 
   3. Decrypt even part using Mono
       P_even_reversed ← Mono_Decrypt(C_even, K2)
 
   4. Reverse even part to restore order
       P_even ← Reverse(P_even_reversed)
 
   5. Rebuild plaintext
       Place P_odd characters in odd positions
       Place P_even characters in even positions
 
   Return P