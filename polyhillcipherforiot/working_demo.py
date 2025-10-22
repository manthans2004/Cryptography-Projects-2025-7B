#!/usr/bin/env python3
"""
Simple Working Interactive Poly-Hill Cipher Demo
Fixed version that works correctly with the actual implementation
"""

from poly_hill_cipher import PolyHillCipher
import re

def clean_input(text):
    """Clean input text for encryption"""
    return re.sub(r'[^A-Z]', '', text.upper())

def main():
    print("=" * 60)
    print("🔐 WORKING POLY-HILL CIPHER DEMONSTRATION")
    print("=" * 60)
    print("Enter any text to see it encrypted and decrypted!")
    print()
    
    while True:
        print("-" * 40)
        user_input = input("🔤 Enter text (or 'quit' to exit): ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for using the demo!")
            break
            
        if not user_input:
            print("❌ Please enter some text!")
            continue
            
        # Clean the input
        cleaned = clean_input(user_input)
        if not cleaned:
            print("❌ No valid letters found! Please use A-Z letters.")
            continue
            
        if len(cleaned) < 2:
            cleaned += 'X'  # Pad short inputs
            
        print(f"\n🔄 Processing: '{user_input}' → '{cleaned}'")
        
        try:
            # Create a new cipher instance for each encryption
            cipher = PolyHillCipher(block_size=2, modulus=26)
            
            # Generate keys
            polynomial_coeffs, hill_matrix = cipher.generate_key(seed=42)  # Fixed seed for consistent results
            
            # Show the keys being used
            print(f"🔑 Polynomial coefficients: {polynomial_coeffs}")
            print(f"🔑 Hill matrix:\n{hill_matrix}")
            
            # Encrypt
            encrypted = cipher.encrypt(cleaned)
            print(f"\n🔒 ENCRYPTED: '{cleaned}' → '{encrypted}'")
            
            # Decrypt to verify
            decrypted = cipher.decrypt(encrypted)
            print(f"🔓 DECRYPTED: '{encrypted}' → '{decrypted}'")
            
            # Verify it worked
            if decrypted == cleaned:
                print("✅ SUCCESS! Encryption and decryption work perfectly!")
            else:
                print("❌ ERROR: Something went wrong with decryption")
                
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            
        print()

if __name__ == "__main__":
    main()