#!/usr/bin/env python3
"""
Interactive Poly-Hill Cipher Demonstration
Student-friendly version with real-time input/output
"""

from poly_hill_cipher import PolyHillCipher
import re

def clean_input(text):
    """Clean input text for encryption"""
    return re.sub(r'[^A-Z]', '', text.upper())

def main():
    print("=" * 60)
    print("🔐 INTERACTIVE POLY-HILL CIPHER DEMONSTRATION")
    print("=" * 60)
    print("Perfect for showing to students and getting real-time results!")
    print()
    
    # Initialize cipher with simple parameters for demonstration
    cipher = PolyHillCipher(block_size=2, modulus=26)
    
    print("🔧 CURRENT SETTINGS:")
    print(f"   Block Size: 2x2")
    print(f"   Modulus: 26")
    print(f"   Keys will be generated automatically")
    print()
    
    while True:
        print("-" * 60)
        print("📝 ENTER YOUR MESSAGE (or 'quit' to exit)")
        print("-" * 60)
        
        user_input = input("🔤 Your text: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Thanks for using the Poly-Hill Cipher demo!")
            break
            
        if not user_input:
            print("❌ Please enter some text!")
            continue
            
        # Clean the input
        cleaned = clean_input(user_input)
        if not cleaned:
            print("❌ No valid letters found! Please use A-Z letters.")
            continue
            
        print(f"\n🔄 PROCESSING: '{user_input}' → '{cleaned}'")
        print()
        
        try:
            # Generate a simple key first
            polynomial_coeffs, hill_matrix = cipher.generate_key()
            print(f"   🔑 Generated keys automatically")
            
            # Encrypt
            print("🔒 ENCRYPTING...")
            encrypted = cipher.encrypt(cleaned)
            print(f"   📤 Result: '{cleaned}' → '{encrypted}'")
            
            # Decrypt to verify
            print("\n🔓 VERIFYING (DECRYPTING)...")
            decrypted = cipher.decrypt(encrypted)
            print(f"   📥 Result: '{encrypted}' → '{decrypted}'")
            
            # Check if it worked
            if decrypted == cleaned:
                print("   ✅ SUCCESS! Encryption/Decryption works perfectly!")
            else:
                print("   ❌ ERROR: Decryption didn't match original")
                
            print()
            
            # Show some analysis
            if len(cleaned) <= 20:  # Only for short inputs
                print("📊 QUICK ANALYSIS:")
                print(f"   • Original length: {len(cleaned)} characters")
                print(f"   • Encrypted length: {len(encrypted)} characters")
                print(f"   • Character changes: {sum(1 for i, (a, b) in enumerate(zip(cleaned, encrypted)) if a != b)}/{len(cleaned)}")
                
                # Show character mapping
                if len(cleaned) <= 10:
                    print("   • Character mapping:")
                    for i, (orig, enc) in enumerate(zip(cleaned, encrypted)):
                        print(f"     {orig} → {enc}")
        
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            
        print("\n" + "="*60)
        print("💡 TIP: Try different words to see how the cipher works!")
        print("   Examples: HELLO, IOT, SENSOR, SECRET, etc.")
        print("="*60)

if __name__ == "__main__":
    main()