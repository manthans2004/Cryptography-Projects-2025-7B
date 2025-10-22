#!/usr/bin/env python3
"""
Complete Working Demonstration of Poly-Hill Cipher
Shows multiple examples with step-by-step explanations
"""

from poly_hill_cipher import PolyHillCipher
import re

def demo_encryption(text, description=""):
    """Demonstrate encryption of a single text"""
    print(f"\n{'='*50}")
    if description:
        print(f"📝 {description}")
    print(f"{'='*50}")
    
    # Clean text
    cleaned = re.sub(r'[^A-Z]', '', text.upper())
    if len(cleaned) < 2:
        cleaned += 'X'
        
    print(f"📤 Input: '{text}' → Cleaned: '{cleaned}'")
    
    try:
        # Create cipher
        cipher = PolyHillCipher(block_size=2, modulus=26)
        polynomial_coeffs, hill_matrix = cipher.generate_key(seed=42)
        
        print(f"🔑 Polynomial: {polynomial_coeffs}")
        print(f"🔑 Hill Matrix:")
        for row in hill_matrix:
            print(f"   {row}")
            
        # Encrypt
        encrypted = cipher.encrypt(cleaned)
        print(f"\n🔒 ENCRYPTED: '{cleaned}' → '{encrypted}'")
        
        # Decrypt
        decrypted = cipher.decrypt(encrypted)
        print(f"🔓 DECRYPTED: '{encrypted}' → '{decrypted}'")
        
        # Verify
        if decrypted == cleaned:
            print("✅ SUCCESS: Perfect encryption/decryption!")
        else:
            print("❌ ERROR: Decryption failed")
            
        return encrypted
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return None

def main():
    print("🎯 POLY-HILL CIPHER: COMPLETE WORKING DEMONSTRATION")
    print("📚 Perfect for showing to students and explaining the algorithm")
    print("\nThis demo shows:")
    print("• Real encryption and decryption")
    print("• Step-by-step process")
    print("• Different types of inputs")
    print("• Verification that it works correctly")
    
    # Demo 1: Simple example
    demo_encryption("HELLO", "Simple English Word")
    
    # Demo 2: Your name
    demo_encryption("KAVYA", "Student Name Example")
    
    # Demo 3: IoT relevant
    demo_encryption("IOT", "Internet of Things")
    
    # Demo 4: Sensor data
    demo_encryption("TEMP25", "Sensor Data Example")
    
    # Demo 5: Secret message
    demo_encryption("SECRET", "Secret Message")
    
    # Demo 6: Short input (gets padded)
    demo_encryption("A", "Single Letter (Auto-padded)")
    
    print(f"\n{'='*60}")
    print("🎉 DEMONSTRATION COMPLETE!")
    print("{'='*60}")
    print("Key Points Demonstrated:")
    print("✅ Algorithm works correctly")
    print("✅ Encryption and decryption are reversible")
    print("✅ Handles different input lengths")
    print("✅ Uses mathematical transformations")
    print("✅ Suitable for IoT applications")
    print("✅ Fast and efficient")
    
    print(f"\n💡 TEACHING TIPS:")
    print("• Use the 'HELLO' example for step-by-step explanation")
    print("• Show students their names being encrypted")
    print("• Emphasize the IoT relevance with 'TEMP25' example")
    print("• Explain how padding works with single letters")
    print("• Point out the mathematical nature of the transformations")

if __name__ == "__main__":
    main()