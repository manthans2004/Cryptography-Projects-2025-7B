"""
Poly-Hill Cipher (PHC): Lightweight Hybrid Cryptography for IoT-Enabled Devices

This module implements the Poly-Hill Cipher algorithm optimized for IoT devices.
It combines polynomial operations with Hill cipher matrix transformations.

Author: Cryptography Implementation
Date: September 2025
"""

import numpy as np
import random
from typing import Tuple, List, Optional, Union, Any
from math import gcd
import string

class PolyHillCipher:
    """
    Poly-Hill Cipher implementation for IoT-enabled devices.
    
    Combines polynomial transformations with Hill cipher matrix operations
    for lightweight yet secure encryption suitable for resource-constrained devices.
    """
    
    def __init__(self, block_size: int = 3, modulus: int = 26):
        """
        Initialize the Poly-Hill Cipher.
        
        Args:
            block_size (int): Size of the square matrix (n×n). Default is 3.
            modulus (int): Modulus for all operations. Default is 26 (for alphabet).
        """
        self.n = block_size
        self.p = modulus
        self.polynomial_coeffs = None
        self.hill_matrix = None
        self.hill_matrix_inv = None
        self.poly_lookup = None
        self.inverse_lookup = None
        
    def generate_key(self, seed: Optional[int] = None) -> Tuple[List[int], Any]:
        """
        Generate cryptographic keys for the Poly-Hill Cipher.
        
        Args:
            seed (int, optional): Random seed for reproducible key generation.
            
        Returns:
            Tuple[List[int], np.ndarray]: Polynomial coefficients and Hill matrix.
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # Generate polynomial coefficients
        self.polynomial_coeffs = [random.randint(1, self.p - 1) for _ in range(self.n + 1)]
        
        # Generate Hill cipher matrix
        while True:
            self.hill_matrix = np.random.randint(0, self.p, size=(self.n, self.n))
            det = int(np.linalg.det(self.hill_matrix)) % self.p
            
            # Ensure matrix is invertible (det != 0 and gcd(det, p) = 1)
            if det != 0 and gcd(det, self.p) == 1:
                break
        
        # Compute and store matrix inverse
        self.hill_matrix_inv = self._matrix_inverse(self.hill_matrix)
        
        # Pre-compute polynomial lookup tables for faster decryption
        self._build_lookup_tables()
        
        return self.polynomial_coeffs, self.hill_matrix
    
    def _build_lookup_tables(self):
        """Build lookup tables for polynomial evaluation and inversion."""
        self.poly_lookup = {}
        self.inverse_lookup = {}
        
        for x in range(self.p):
            # Compute P(x) mod p
            poly_value = 0
            for i, coeff in enumerate(self.polynomial_coeffs):
                poly_value = (poly_value + coeff * (x ** i)) % self.p
            
            self.poly_lookup[x] = poly_value
            self.inverse_lookup[poly_value] = x
    
    def _polynomial_transform(self, x: int) -> int:
        """
        Apply polynomial transformation P(x) mod p.
        
        Args:
            x (int): Input value.
            
        Returns:
            int: P(x) mod p
        """
        return self.poly_lookup[x % self.p]
    
    def _inverse_polynomial_transform(self, y: int) -> int:
        """
        Find x such that P(x) ≡ y (mod p).
        
        Args:
            y (int): Output of polynomial transformation.
            
        Returns:
            int: Original input x.
        """
        return self.inverse_lookup.get(y % self.p, 0)
    
    def _matrix_inverse(self, matrix: Any) -> Any:
        """
        Compute modular inverse of matrix.
        
        Args:
            matrix (np.ndarray): Input matrix.
            
        Returns:
            np.ndarray: Modular inverse matrix.
        """
        det = int(np.linalg.det(matrix)) % self.p
        det_inv = self._mod_inverse(det, self.p)
        
        # Compute adjugate matrix
        adj_matrix = np.zeros_like(matrix)
        for i in range(self.n):
            for j in range(self.n):
                minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                cofactor = ((-1) ** (i + j)) * int(np.linalg.det(minor))
                adj_matrix[j][i] = (cofactor * det_inv) % self.p
        
        return adj_matrix.astype(int)
    
    def _mod_inverse(self, a: int, m: int) -> int:
        """
        Compute modular multiplicative inverse using extended Euclidean algorithm.
        
        Args:
            a (int): Number to find inverse of.
            m (int): Modulus.
            
        Returns:
            int: Modular inverse of a mod m.
        """
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            raise ValueError("Modular inverse does not exist")
        return (x % m + m) % m
    
    def _text_to_numbers(self, text: str) -> List[int]:
        """
        Convert text to numerical values.
        
        Args:
            text (str): Input text.
            
        Returns:
            List[int]: Numerical representation.
        """
        # Convert to uppercase and filter only alphabetic characters
        text = ''.join(c.upper() for c in text if c.isalpha())
        return [ord(c) - ord('A') for c in text]
    
    def _numbers_to_text(self, numbers: List[int]) -> str:
        """
        Convert numerical values back to text.
        
        Args:
            numbers (List[int]): Numerical values.
            
        Returns:
            str: Text representation.
        """
        return ''.join(chr((num % self.p) + ord('A')) for num in numbers)
    
    def _pad_text(self, numbers: List[int]) -> List[int]:
        """
        Pad the numerical text to be multiple of block size.
        
        Args:
            numbers (List[int]): Input numbers.
            
        Returns:
            List[int]: Padded numbers.
        """
        while len(numbers) % self.n != 0:
            numbers.append(23)  # Pad with 'X'
        return numbers
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using Poly-Hill Cipher.
        
        Args:
            plaintext (str): Input plaintext.
            
        Returns:
            str: Encrypted ciphertext.
        """
        if self.polynomial_coeffs is None or self.hill_matrix is None:
            raise ValueError("Keys not generated. Call generate_key() first.")
        
        # Convert text to numbers and pad
        numbers = self._text_to_numbers(plaintext)
        numbers = self._pad_text(numbers)
        
        encrypted_numbers = []
        
        # Process in blocks
        for i in range(0, len(numbers), self.n):
            block = numbers[i:i + self.n]
            
            # Step 1: Apply polynomial transformation
            poly_block = [self._polynomial_transform(x) for x in block]
            
            # Step 2: Apply Hill cipher matrix transformation
            block_vector = np.array(poly_block).reshape(self.n, 1)
            hill_result = (self.hill_matrix @ block_vector) % self.p
            
            # Step 3: Apply position-dependent obfuscation
            block_index = i // self.n
            obfuscated_block = []
            for j, val in enumerate(hill_result.flatten()):
                obfuscated_val = val ^ ((block_index + j) % self.p)
                obfuscated_block.append(obfuscated_val % self.p)
            
            encrypted_numbers.extend(obfuscated_block)
        
        return self._numbers_to_text(encrypted_numbers)
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext using Poly-Hill Cipher.
        
        Args:
            ciphertext (str): Input ciphertext.
            
        Returns:
            str: Decrypted plaintext.
        """
        if self.hill_matrix_inv is None:
            raise ValueError("Keys not generated. Call generate_key() first.")
        
        # Convert ciphertext to numbers
        numbers = self._text_to_numbers(ciphertext)
        decrypted_numbers = []
        
        # Process in blocks
        for i in range(0, len(numbers), self.n):
            block = numbers[i:i + self.n]
            block_index = i // self.n
            
            # Step 1: Reverse position-dependent obfuscation
            deobfuscated_block = []
            for j, val in enumerate(block):
                original_val = val ^ ((block_index + j) % self.p)
                deobfuscated_block.append(original_val % self.p)
            
            # Step 2: Apply inverse Hill cipher transformation
            block_vector = np.array(deobfuscated_block).reshape(self.n, 1)
            hill_result = (self.hill_matrix_inv @ block_vector) % self.p
            
            # Step 3: Apply inverse polynomial transformation
            original_block = []
            for val in hill_result.flatten():
                original_val = self._inverse_polynomial_transform(int(val))
                original_block.append(original_val)
            
            decrypted_numbers.extend(original_block)
        
        # Convert back to text and remove padding
        decrypted_text = self._numbers_to_text(decrypted_numbers)
        return decrypted_text.rstrip('X')  # Remove padding
    
    def get_key_info(self) -> dict:
        """
        Get information about the current keys.
        
        Returns:
            dict: Key information including polynomial coefficients and matrix.
        """
        return {
            'polynomial_coefficients': self.polynomial_coeffs,
            'hill_matrix': self.hill_matrix.tolist() if self.hill_matrix is not None else None,
            'block_size': self.n,
            'modulus': self.p
        }
    
    def set_keys(self, polynomial_coeffs: List[int], hill_matrix: List[List[int]]):
        """
        Set keys manually (for testing or key exchange).
        
        Args:
            polynomial_coeffs (List[int]): Polynomial coefficients.
            hill_matrix (List[List[int]]): Hill cipher matrix.
        """
        self.polynomial_coeffs = polynomial_coeffs
        self.hill_matrix = np.array(hill_matrix)
        self.hill_matrix_inv = self._matrix_inverse(self.hill_matrix)
        self._build_lookup_tables()


# IoT-Optimized Version for Memory-Constrained Devices
class IoTPolyHillCipher(PolyHillCipher):
    """
    Memory-optimized version of Poly-Hill Cipher for IoT devices.
    
    Uses smaller block sizes and simplified operations to reduce
    memory footprint and computational requirements.
    """
    
    def __init__(self, block_size: int = 2, modulus: int = 26):
        """
        Initialize IoT-optimized Poly-Hill Cipher.
        
        Args:
            block_size (int): Smaller block size for IoT. Default is 2.
            modulus (int): Modulus for operations. Default is 26.
        """
        super().__init__(block_size, modulus)
        self.memory_efficient = True
    
    def encrypt_stream(self, plaintext_stream: str, chunk_size: int = 64) -> str:
        """
        Stream-based encryption for continuous IoT data.
        
        Args:
            plaintext_stream (str): Input stream.
            chunk_size (int): Size of chunks to process.
            
        Returns:
            str: Encrypted stream.
        """
        result = ""
        for i in range(0, len(plaintext_stream), chunk_size):
            chunk = plaintext_stream[i:i + chunk_size]
            result += self.encrypt(chunk)
        return result
    
    def get_memory_usage(self) -> dict:
        """
        Estimate memory usage for IoT resource planning.
        
        Returns:
            dict: Memory usage statistics.
        """
        poly_memory = len(self.polynomial_coeffs) * 4  # 4 bytes per int
        matrix_memory = self.n * self.n * 4 * 2  # Matrix + inverse
        lookup_memory = self.p * 4 * 2  # Forward + inverse lookup
        
        return {
            'polynomial_coefficients': poly_memory,
            'hill_matrices': matrix_memory,
            'lookup_tables': lookup_memory,
            'total_bytes': poly_memory + matrix_memory + lookup_memory
        }