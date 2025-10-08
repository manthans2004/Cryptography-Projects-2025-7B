# Poly-Hill Cipher (PHC): Lightweight Hybrid Cryptography for IoT

## Overview

The Poly-Hill Cipher (PHC) is a hybrid cryptographic algorithm that combines polynomial operations with Hill cipher matrix transformations, specifically designed for IoT-enabled devices with limited computational resources.

## Mathematical Foundation

### Core Components

1. **Polynomial Layer**: Uses polynomial arithmetic over finite fields for initial transformation
2. **Hill Cipher Layer**: Applies matrix operations for further obfuscation
3. **Modular Operations**: All computations performed modulo a prime number for efficiency

### Algorithm Specification

#### Key Generation
```
INPUT: Security parameter n (key size)
OUTPUT: Key tuple (P, K, p)

1. Generate polynomial P(x) = a₀ + a₁x + a₂x² + ... + aₙxⁿ
   where coefficients aᵢ are randomly selected from [1, 25]

2. Generate Hill cipher key matrix K (n×n)
   - Randomly fill matrix with values [0, 25]
   - Ensure det(K) ≠ 0 and gcd(det(K), 26) = 1

3. Select modulus p (small prime, typically 26 for alphabetic text)

RETURN (P, K, p)
```

#### Encryption Process
```
INPUT: Plaintext M, Key (P, K, p)
OUTPUT: Ciphertext C

1. TEXT PREPROCESSING:
   - Convert plaintext to numerical values (A=0, B=1, ..., Z=25)
   - Pad text to multiple of matrix size n

2. POLYNOMIAL TRANSFORMATION:
   For each block Bᵢ of size n:
   - Apply polynomial: B'ᵢ[j] = P(Bᵢ[j]) mod p
   
3. MATRIX TRANSFORMATION:
   - Arrange B'ᵢ as column vector
   - Compute: C'ᵢ = K × B'ᵢ mod p

4. FINAL OBFUSCATION:
   - Apply lightweight XOR with position-dependent mask
   - Cᵢ[j] = C'ᵢ[j] ⊕ (i + j) mod p

RETURN concatenated ciphertext blocks
```

#### Decryption Process
```
INPUT: Ciphertext C, Key (P, K, p)
OUTPUT: Plaintext M

1. REVERSE OBFUSCATION:
   For each block Cᵢ:
   - C'ᵢ[j] = Cᵢ[j] ⊕ (i + j) mod p

2. INVERSE MATRIX TRANSFORMATION:
   - Compute K⁻¹ (modular inverse of K)
   - B'ᵢ = K⁻¹ × C'ᵢ mod p

3. INVERSE POLYNOMIAL TRANSFORMATION:
   - For each element, find x such that P(x) ≡ B'ᵢ[j] (mod p)
   - Use lookup table or iterative search

4. TEXT RECONSTRUCTION:
   - Convert numerical values back to characters
   - Remove padding

RETURN plaintext M
```

## Security Features

### Strength Components
1. **Double Layer Protection**: Polynomial + Matrix transformations
2. **Key Space**: Large keyspace due to polynomial coefficients and matrix elements
3. **Confusion**: Polynomial operations provide non-linear transformation
4. **Diffusion**: Matrix multiplication spreads influence across block

### IoT Optimizations
1. **Low Memory**: Fixed-size matrices and polynomial coefficients
2. **Fast Operations**: Simple arithmetic operations (add, multiply, mod)
3. **Scalable Key Size**: Adjustable n for security vs. performance trade-off
4. **Parallel Processing**: Block-based operation enables parallel execution

## Complexity Analysis

### Time Complexity
- **Key Generation**: O(n²)
- **Encryption**: O(m × n²) where m = number of blocks
- **Decryption**: O(m × n²) + O(n × p) for polynomial inversion

### Space Complexity
- **Memory Usage**: O(n²) for key storage
- **Working Memory**: O(n) per block processing

## Implementation Considerations

### For IoT Devices
1. Use small block sizes (n = 2 or 3) for memory-constrained devices
2. Pre-compute polynomial lookup tables for faster decryption
3. Implement fixed-point arithmetic to avoid floating-point operations
4. Use circular buffers for stream processing

### Security Parameters
- Minimum n = 2 for basic security
- Recommended n = 3-4 for standard IoT applications
- Use p = 26 for text, p = 256 for binary data
- Polynomial degree should equal block size for optimal mixing

## Advantages for IoT

1. **Lightweight**: Minimal computational overhead
2. **Energy Efficient**: Simple operations reduce power consumption  
3. **Scalable**: Adjustable security level based on device capabilities
4. **Fast**: Suitable for real-time IoT communication
5. **Robust**: Multiple transformation layers provide good security

## Limitations

1. **Block-based**: Vulnerable to pattern analysis with identical blocks
2. **Small Key Space**: Limited by IoT computational constraints
3. **Known Structure**: Attackers knowing the algorithm structure may exploit it
4. **Polynomial Inversion**: Decryption slightly more complex than encryption