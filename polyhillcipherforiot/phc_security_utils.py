"""
Security Utilities for Poly-Hill Cipher

This module provides additional security functions and analysis tools
for the Poly-Hill Cipher implementation.

Author: Cryptography Implementation  
Date: September 2025
"""

import numpy as np
import random
from typing import List, Dict, Tuple, Any
import hashlib
import secrets
from collections import Counter

class PHCSecurityUtils:
    """Security utilities and analysis tools for Poly-Hill Cipher."""
    
    @staticmethod
    def generate_secure_polynomial(degree: int, modulus: int, entropy_source: str = None) -> List[int]:
        """
        Generate cryptographically secure polynomial coefficients.
        
        Args:
            degree (int): Degree of polynomial.
            modulus (int): Modulus for coefficients.
            entropy_source (str): Additional entropy source.
            
        Returns:
            List[int]: Secure polynomial coefficients.
        """
        if entropy_source:
            # Use additional entropy for coefficient generation
            seed_material = entropy_source.encode() + secrets.token_bytes(32)
            hash_obj = hashlib.sha256(seed_material)
            seed = int.from_bytes(hash_obj.digest()[:4], 'big')
            random.seed(seed)
        
        coefficients = []
        for _ in range(degree + 1):
            # Ensure coefficients are non-zero and coprime to modulus
            while True:
                coeff = secrets.randbelow(modulus - 1) + 1
                if PHCSecurityUtils.gcd(coeff, modulus) == 1:
                    coefficients.append(coeff)
                    break
        
        return coefficients
    
    @staticmethod
    def generate_secure_matrix(size: int, modulus: int) -> Any:
        """
        Generate cryptographically secure invertible matrix.
        
        Args:
            size (int): Matrix dimension (n×n).
            modulus (int): Modulus for matrix elements.
            
        Returns:
            np.ndarray: Secure invertible matrix.
        """
        max_attempts = 1000
        attempts = 0
        
        while attempts < max_attempts:
            # Generate random matrix with secure random numbers
            matrix = np.array([[secrets.randbelow(modulus) for _ in range(size)] 
                              for _ in range(size)])
            
            det = int(np.linalg.det(matrix)) % modulus
            
            # Check if matrix is invertible
            if det != 0 and PHCSecurityUtils.gcd(det, modulus) == 1:
                return matrix
            
            attempts += 1
        
        raise ValueError(f"Could not generate invertible matrix after {max_attempts} attempts")
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """
        Compute greatest common divisor using Euclidean algorithm.
        
        Args:
            a (int): First number.
            b (int): Second number.
            
        Returns:
            int: GCD of a and b.
        """
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def analyze_frequency(ciphertext: str) -> Dict[str, float]:
        """
        Analyze frequency distribution of ciphertext.
        
        Args:
            ciphertext (str): Input ciphertext.
            
        Returns:
            Dict[str, float]: Character frequency analysis.
        """
        counter = Counter(ciphertext.upper())
        total = len(ciphertext)
        
        frequencies = {}
        for char, count in counter.items():
            frequencies[char] = count / total
        
        return dict(sorted(frequencies.items()))
    
    @staticmethod
    def calculate_index_of_coincidence(text: str) -> float:
        """
        Calculate Index of Coincidence for cryptanalysis resistance.
        
        Args:
            text (str): Input text.
            
        Returns:
            float: Index of Coincidence value.
        """
        text = text.upper().replace(' ', '')
        n = len(text)
        
        if n <= 1:
            return 0.0
        
        counter = Counter(text)
        ic = sum(count * (count - 1) for count in counter.values())
        ic = ic / (n * (n - 1))
        
        return ic
    
    @staticmethod
    def entropy_analysis(ciphertext: str) -> Dict[str, float]:
        """
        Calculate entropy metrics for randomness assessment.
        
        Args:
            ciphertext (str): Input ciphertext.
            
        Returns:
            Dict[str, float]: Entropy analysis results.
        """
        frequencies = PHCSecurityUtils.analyze_frequency(ciphertext)
        
        # Shannon entropy
        shannon_entropy = 0
        for freq in frequencies.values():
            if freq > 0:
                shannon_entropy -= freq * np.log2(freq)
        
        # Maximum possible entropy for alphabet
        max_entropy = np.log2(26)  # For 26 letters
        
        # Relative entropy
        relative_entropy = shannon_entropy / max_entropy if max_entropy > 0 else 0
        
        return {
            'shannon_entropy': shannon_entropy,
            'max_entropy': max_entropy,
            'relative_entropy': relative_entropy,
            'randomness_score': relative_entropy
        }
    
    @staticmethod
    def avalanche_test(cipher, plaintext: str, num_tests: int = 100) -> Dict[str, float]:
        """
        Perform avalanche effect test on the cipher.
        
        Args:
            cipher: PHC cipher instance.
            plaintext (str): Test plaintext.
            num_tests (int): Number of tests to perform.
            
        Returns:
            Dict[str, float]: Avalanche test results.
        """
        if not plaintext:
            return {'error': 'Empty plaintext'}
        
        original_ciphertext = cipher.encrypt(plaintext)
        avalanche_ratios = []
        
        for _ in range(num_tests):
            # Modify one random character
            modified_plaintext = list(plaintext)
            if len(modified_plaintext) > 0:
                pos = random.randint(0, len(modified_plaintext) - 1)
                # Change to a different random character
                original_char = modified_plaintext[pos]
                while True:
                    new_char = chr(random.randint(ord('A'), ord('Z')))
                    if new_char != original_char:
                        modified_plaintext[pos] = new_char
                        break
                
                modified_ciphertext = cipher.encrypt(''.join(modified_plaintext))
                
                # Count different bits/characters
                if len(original_ciphertext) == len(modified_ciphertext):
                    diff_count = sum(1 for a, b in zip(original_ciphertext, modified_ciphertext) if a != b)
                    avalanche_ratio = diff_count / len(original_ciphertext)
                    avalanche_ratios.append(avalanche_ratio)
        
        if avalanche_ratios:
            return {
                'average_avalanche_ratio': np.mean(avalanche_ratios),
                'min_avalanche_ratio': min(avalanche_ratios),
                'max_avalanche_ratio': max(avalanche_ratios),
                'std_avalanche_ratio': np.std(avalanche_ratios),
                'ideal_ratio': 0.5  # Ideal avalanche effect
            }
        else:
            return {'error': 'No valid tests performed'}
    
    @staticmethod
    def key_strength_analysis(polynomial_coeffs: List[int], hill_matrix: Any, modulus: int) -> Dict[str, any]:
        """
        Analyze the strength of generated keys.
        
        Args:
            polynomial_coeffs (List[int]): Polynomial coefficients.
            hill_matrix (np.ndarray): Hill cipher matrix.
            modulus (int): Modulus value.
            
        Returns:
            Dict[str, any]: Key strength analysis.
        """
        analysis = {}
        
        # Polynomial analysis
        analysis['polynomial'] = {
            'degree': len(polynomial_coeffs) - 1,
            'coefficients_gcd': PHCSecurityUtils.gcd_list(polynomial_coeffs),
            'all_coprime_to_modulus': all(PHCSecurityUtils.gcd(c, modulus) == 1 for c in polynomial_coeffs),
            'coefficient_distribution': PHCSecurityUtils.analyze_distribution(polynomial_coeffs, modulus)
        }
        
        # Matrix analysis
        det = int(np.linalg.det(hill_matrix)) % modulus
        analysis['matrix'] = {
            'determinant': det,
            'invertible': det != 0 and PHCSecurityUtils.gcd(det, modulus) == 1,
            'condition_number': np.linalg.cond(hill_matrix.astype(float)),
            'element_distribution': PHCSecurityUtils.analyze_distribution(hill_matrix.flatten(), modulus)
        }
        
        # Overall key space
        poly_space = modulus ** len(polynomial_coeffs)
        matrix_space = modulus ** (hill_matrix.size)
        analysis['key_space'] = {
            'polynomial_space': poly_space,
            'matrix_space': matrix_space,
            'total_space': poly_space * matrix_space,
            'key_space_bits': np.log2(poly_space * matrix_space)
        }
        
        return analysis
    
    @staticmethod
    def gcd_list(numbers: List[int]) -> int:
        """
        Compute GCD of a list of numbers.
        
        Args:
            numbers (List[int]): List of integers.
            
        Returns:
            int: GCD of all numbers.
        """
        result = numbers[0]
        for i in range(1, len(numbers)):
            result = PHCSecurityUtils.gcd(result, numbers[i])
        return result
    
    @staticmethod
    def analyze_distribution(values: Any, modulus: int) -> Dict[str, float]:
        """
        Analyze statistical distribution of values.
        
        Args:
            values (np.ndarray): Input values.
            modulus (int): Expected range [0, modulus-1].
            
        Returns:
            Dict[str, float]: Distribution analysis.
        """
        values_flat = values.flatten() if isinstance(values, np.ndarray) else np.array(values)
        
        return {
            'mean': float(np.mean(values_flat)),
            'std': float(np.std(values_flat)),
            'min': float(np.min(values_flat)),
            'max': float(np.max(values_flat)),
            'expected_mean': (modulus - 1) / 2,
            'uniformity_score': 1.0 - abs(np.mean(values_flat) - (modulus - 1) / 2) / ((modulus - 1) / 2)
        }


class PHCCryptanalysisResistance:
    """Tools for testing cryptanalysis resistance."""
    
    @staticmethod
    def brute_force_complexity(key_space_bits: float) -> Dict[str, str]:
        """
        Estimate brute force attack complexity.
        
        Args:
            key_space_bits (float): Size of key space in bits.
            
        Returns:
            Dict[str, str]: Complexity estimates.
        """
        operations = 2 ** key_space_bits
        
        # Assuming 1 billion operations per second
        seconds = operations / 1e9
        years = seconds / (365.25 * 24 * 3600)
        
        return {
            'key_space_size': f"2^{key_space_bits:.1f}",
            'operations_required': f"{operations:.2e}",
            'time_at_1GHz': f"{years:.2e} years",
            'security_level': "High" if key_space_bits > 80 else "Medium" if key_space_bits > 64 else "Low"
        }
    
    @staticmethod
    def known_plaintext_resistance(cipher, known_pairs: List[Tuple[str, str]]) -> Dict[str, any]:
        """
        Test resistance against known plaintext attacks.
        
        Args:
            cipher: PHC cipher instance.
            known_pairs (List[Tuple[str, str]]): List of (plaintext, ciphertext) pairs.
            
        Returns:
            Dict[str, any]: Resistance analysis.
        """
        # This is a simplified test - in practice, more sophisticated analysis would be needed
        consistent_encryptions = 0
        
        for plaintext, expected_ciphertext in known_pairs:
            try:
                actual_ciphertext = cipher.encrypt(plaintext)
                if actual_ciphertext == expected_ciphertext:
                    consistent_encryptions += 1
            except:
                pass
        
        return {
            'total_pairs_tested': len(known_pairs),
            'consistent_encryptions': consistent_encryptions,
            'consistency_rate': consistent_encryptions / len(known_pairs) if known_pairs else 0,
            'resistance_level': "Good" if consistent_encryptions == len(known_pairs) else "Poor"
        }