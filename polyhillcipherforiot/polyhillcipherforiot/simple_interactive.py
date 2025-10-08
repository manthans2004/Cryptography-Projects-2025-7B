#!/usr/bin/env python3
"""
Simple Interactive Poly-Hill Cipher Demo
Enter your own text and see it encrypted!
"""

import re

def simple_encrypt(text):
    """Simple demonstration encryption (not the full PHC algorithm)"""
    # Clean text
    cleaned = re.sub(r'[^A-Z]', '', text.upper())
    if not cleaned:
        return "ERROR: No valid letters"
    
    # Simple Caesar-like transformation for demo
    result = ""
    for i, char in enumerate(cleaned):
        # Simple shift based on position
        shift = (ord(char) - ord('A') + i + 5) % 26
        result += chr(shift + ord('A'))
    
    return result

def main():
    print("=" * 50)
    print("🔐 INTERACTIVE ENCRYPTION DEMO")
    print("=" * 50)
    print("Enter any text to see it encrypted!")
    print("(Type 'quit' to exit)")
    print()
    
    while True:
        print("-" * 30)
        user_input = input("🔤 Enter your text: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
            
        if not user_input:
            print("❌ Please enter some text!")
            continue
            
        print(f"\n🔄 Processing: '{user_input}'")
        encrypted = simple_encrypt(user_input)
        print(f"🔒 Encrypted: '{encrypted}'")
        print(f"✅ '{user_input}' → '{encrypted}'")
        print()

if __name__ == "__main__":
    main()