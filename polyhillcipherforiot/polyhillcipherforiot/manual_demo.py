#!/usr/bin/env python3
"""
Manual Step-by-Step Demonstration
Perfect for explaining to students with hand calculations
"""

print("🎓 POLY-HILL CIPHER: STEP-BY-STEP MANUAL DEMONSTRATION")
print("=" * 60)
print("Perfect for teaching students the algorithm!")
print()

print("📝 EXAMPLE: Encrypt 'HI'")
print("-" * 30)
print("Given:")
print("  • Polynomial: P(x) = 1 + 2x")  
print("  • Hill Matrix: [[3, 2], [1, 1]]")
print("  • Modulus: 26")
print()

print("STEP 1: Convert letters to numbers")
print("  H = 7, I = 8")
print("  Block: [7, 8]")
print()

print("STEP 2: Apply polynomial P(x) = 1 + 2x")
print("  P(7) = 1 + 2×7 = 15")
print("  P(8) = 1 + 2×8 = 17") 
print("  After polynomial: [15, 17]")
print()

print("STEP 3: Apply Hill matrix")
print("  [3 2] × [15] = [3×15 + 2×17] = [45 + 34] = [79]")
print("  [1 1]   [17]   [1×15 + 1×17]   [15 + 17]   [32]")
print("  Mod 26: [79 mod 26, 32 mod 26] = [1, 6]")
print()

print("STEP 4: Position obfuscation (XOR)")
print("  1 ⊕ 0 = 1 (first position)")
print("  6 ⊕ 1 = 7 (second position)") 
print("  After obfuscation: [1, 7]")
print()

print("STEP 5: Convert back to letters")
print("  1 → B, 7 → H")
print("  Result: 'HI' → 'BH'")
print()

print("✅ FINAL RESULT: 'HI' encrypts to 'BH'")
print()

print("🎯 KEY TEACHING POINTS:")
print("• Each step transforms the data mathematically")
print("• Polynomial adds confusion (scrambles meaning)")
print("• Matrix adds diffusion (spreads changes)")
print("• XOR adds position-dependent randomness") 
print("• Perfect for IoT: fast, lightweight, secure")
print()

print("💡 STUDENT EXERCISE:")
print("Try encrypting 'GO' using the same steps!")
print("G=6, O=14 → P(6)=13, P(14)=29≡3 → Matrix math → Result")

print("\n" + "=" * 60)
print("🎉 Use this manual example to explain the algorithm!")
print("Students can follow along with pencil and paper!")