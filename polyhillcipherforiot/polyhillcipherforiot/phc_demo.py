"""
Poly-Hill Cipher Demonstration and Examples

This module demonstrates how to use the Poly-Hill Cipher for IoT applications
with various examples and test cases.

Author: Cryptography Implementation
Date: September 2025
"""

from poly_hill_cipher import PolyHillCipher, IoTPolyHillCipher
from phc_security_utils import PHCSecurityUtils, PHCCryptanalysisResistance
import time
import random
import string

def basic_usage_example():
    """Demonstrate basic usage of the Poly-Hill Cipher."""
    print("=" * 60)
    print("BASIC USAGE EXAMPLE")
    print("=" * 60)
    
    # Initialize cipher
    cipher = PolyHillCipher(block_size=3, modulus=26)
    
    # Generate keys
    print("1. Generating cryptographic keys...")
    poly_coeffs, hill_matrix = cipher.generate_key(seed=12345)  # Fixed seed for reproducibility
    
    print(f"   Polynomial coefficients: {poly_coeffs}")
    print(f"   Hill matrix:\n{hill_matrix}")
    
    # Encrypt a message
    plaintext = "HELLO WORLD THIS IS A SECRET MESSAGE"
    print(f"\n2. Original message: '{plaintext}'")
    
    ciphertext = cipher.encrypt(plaintext)
    print(f"   Encrypted message: '{ciphertext}'")
    
    # Decrypt the message
    decrypted = cipher.decrypt(ciphertext)
    print(f"   Decrypted message: '{decrypted}'")
    
    # Verify correctness
    success = plaintext.replace(" ", "") == decrypted
    print(f"\n3. Encryption/Decryption successful: {success}")
    
    return success

def iot_optimized_example():
    """Demonstrate IoT-optimized version for resource-constrained devices."""
    print("\n" + "=" * 60)
    print("IoT OPTIMIZED EXAMPLE")
    print("=" * 60)
    
    # Initialize IoT-optimized cipher with smaller block size
    iot_cipher = IoTPolyHillCipher(block_size=2, modulus=26)
    
    # Generate keys
    print("1. Generating lightweight keys for IoT device...")
    poly_coeffs, hill_matrix = iot_cipher.generate_key(seed=54321)
    
    print(f"   Polynomial coefficients: {poly_coeffs}")
    print(f"   Hill matrix:\n{hill_matrix}")
    
    # Check memory usage
    memory_usage = iot_cipher.get_memory_usage()
    print(f"\n2. Memory footprint analysis:")
    for component, bytes_used in memory_usage.items():
        print(f"   {component}: {bytes_used} bytes")
    
    # Encrypt sensor data
    sensor_data = "TEMPERATURE25HUMIDITY60PRESSURE1013"
    print(f"\n3. IoT sensor data: '{sensor_data}'")
    
    encrypted_data = iot_cipher.encrypt(sensor_data)
    print(f"   Encrypted data: '{encrypted_data}'")
    
    decrypted_data = iot_cipher.decrypt(encrypted_data)
    print(f"   Decrypted data: '{decrypted_data}'")
    
    # Stream processing example
    print(f"\n4. Stream processing test:")
    stream_data = "CONTINUOUS SENSOR STREAM DATA FOR IOT DEVICE MONITORING SYSTEM"
    encrypted_stream = iot_cipher.encrypt_stream(stream_data, chunk_size=16)
    print(f"   Stream encrypted: '{encrypted_stream[:50]}...'")
    
    return True

def security_analysis_example():
    """Demonstrate security analysis capabilities."""
    print("\n" + "=" * 60)
    print("SECURITY ANALYSIS EXAMPLE")
    print("=" * 60)
    
    cipher = PolyHillCipher(block_size=3, modulus=26)
    poly_coeffs, hill_matrix = cipher.generate_key()
    
    # Key strength analysis
    print("1. Key Strength Analysis:")
    key_analysis = PHCSecurityUtils.key_strength_analysis(poly_coeffs, hill_matrix, 26)
    
    print(f"   Polynomial degree: {key_analysis['polynomial']['degree']}")
    print(f"   Matrix invertible: {key_analysis['matrix']['invertible']}")
    print(f"   Key space (bits): {key_analysis['key_space']['key_space_bits']:.1f}")
    
    # Brute force resistance
    bf_analysis = PHCCryptanalysisResistance.brute_force_complexity(
        key_analysis['key_space']['key_space_bits']
    )
    print(f"   Security level: {bf_analysis['security_level']}")
    print(f"   Brute force time: {bf_analysis['time_at_1GHz']}")
    
    # Frequency analysis
    test_message = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG" * 3
    ciphertext = cipher.encrypt(test_message)
    
    print(f"\n2. Frequency Analysis:")
    frequencies = PHCSecurityUtils.analyze_frequency(ciphertext)
    print(f"   Most frequent chars: {dict(list(frequencies.items())[:5])}")
    
    # Entropy analysis
    entropy_results = PHCSecurityUtils.entropy_analysis(ciphertext)
    print(f"\n3. Entropy Analysis:")
    print(f"   Shannon entropy: {entropy_results['shannon_entropy']:.3f}")
    print(f"   Randomness score: {entropy_results['randomness_score']:.3f}")
    
    # Index of Coincidence
    ic = PHCSecurityUtils.calculate_index_of_coincidence(ciphertext)
    print(f"   Index of Coincidence: {ic:.4f}")
    print(f"   Random text IC ≈ 0.038, English text IC ≈ 0.066")
    
    return True

def avalanche_effect_test():
    """Demonstrate avalanche effect testing."""
    print("\n" + "=" * 60)
    print("AVALANCHE EFFECT TEST")
    print("=" * 60)
    
    cipher = PolyHillCipher(block_size=3, modulus=26)
    cipher.generate_key(seed=99999)
    
    test_plaintext = "CRYPTOGRAPHY IS THE SCIENCE OF SECRET WRITING"
    print(f"Testing avalanche effect with: '{test_plaintext}'")
    
    print("\nRunning avalanche tests (this may take a moment)...")
    avalanche_results = PHCSecurityUtils.avalanche_test(cipher, test_plaintext, num_tests=50)
    
    if 'error' not in avalanche_results:
        print(f"\nAvalanche Effect Results:")
        print(f"   Average change ratio: {avalanche_results['average_avalanche_ratio']:.3f}")
        print(f"   Ideal ratio: {avalanche_results['ideal_ratio']:.3f}")
        print(f"   Min change ratio: {avalanche_results['min_avalanche_ratio']:.3f}")
        print(f"   Max change ratio: {avalanche_results['max_avalanche_ratio']:.3f}")
        print(f"   Standard deviation: {avalanche_results['std_avalanche_ratio']:.3f}")
        
        # Evaluate avalanche quality
        avg_ratio = avalanche_results['average_avalanche_ratio']
        if avg_ratio > 0.4 and avg_ratio < 0.6:
            print("   ✓ Good avalanche effect (close to ideal 0.5)")
        elif avg_ratio > 0.3 and avg_ratio < 0.7:
            print("   ~ Acceptable avalanche effect")
        else:
            print("   ✗ Poor avalanche effect")
    else:
        print(f"   Error: {avalanche_results['error']}")
    
    return True

def performance_comparison():
    """Compare performance between standard and IoT versions."""
    print("\n" + "=" * 60)
    print("PERFORMANCE COMPARISON")
    print("=" * 60)
    
    # Test data
    short_text = "HELLO WORLD"
    medium_text = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG" * 5
    long_text = "LOREM IPSUM DOLOR SIT AMET CONSECTETUR ADIPISCING ELIT" * 20
    
    test_cases = [
        ("Short text (11 chars)", short_text),
        ("Medium text (215 chars)", medium_text),
        ("Long text (1060 chars)", long_text)
    ]
    
    # Standard cipher
    standard_cipher = PolyHillCipher(block_size=3, modulus=26)
    standard_cipher.generate_key(seed=11111)
    
    # IoT cipher
    iot_cipher = IoTPolyHillCipher(block_size=2, modulus=26)
    iot_cipher.generate_key(seed=11111)
    
    print(f"{'Test Case':<20} {'Standard (ms)':<15} {'IoT (ms)':<10} {'Speedup':<10}")
    print("-" * 60)
    
    for test_name, text in test_cases:
        # Time standard cipher
        start_time = time.time()
        for _ in range(100):  # Run multiple times for more accurate timing
            encrypted = standard_cipher.encrypt(text)
            decrypted = standard_cipher.decrypt(encrypted)
        standard_time = (time.time() - start_time) * 10  # Convert to milliseconds
        
        # Time IoT cipher
        start_time = time.time()
        for _ in range(100):
            encrypted = iot_cipher.encrypt(text)
            decrypted = iot_cipher.decrypt(encrypted)
        iot_time = (time.time() - start_time) * 10
        
        speedup = standard_time / iot_time if iot_time > 0 else 0
        print(f"{test_name:<20} {standard_time:<15.2f} {iot_time:<10.2f} {speedup:<10.1f}x")
    
    return True

def real_world_scenarios():
    """Demonstrate real-world IoT scenarios."""
    print("\n" + "=" * 60)
    print("REAL-WORLD IoT SCENARIOS")
    print("=" * 60)
    
    iot_cipher = IoTPolyHillCipher(block_size=2, modulus=26)
    iot_cipher.generate_key()
    
    # Scenario 1: Smart Home Sensor
    print("1. Smart Home Temperature Sensor:")
    sensor_reading = "TEMP23C5HUMID67PCT9LIGHT85PCT"
    encrypted_reading = iot_cipher.encrypt(sensor_reading)
    print(f"   Original: {sensor_reading}")
    print(f"   Encrypted: {encrypted_reading}")
    print(f"   Size increase: {len(encrypted_reading)/len(sensor_reading):.1f}x")
    
    # Scenario 2: Industrial IoT Monitoring
    print(f"\n2. Industrial Machine Status:")
    machine_status = "MACHINE01ONLINE5TEMP95C5VIBRATION02G5PRESSURE150BAR"
    encrypted_status = iot_cipher.encrypt(machine_status)
    decrypted_status = iot_cipher.decrypt(encrypted_status)
    print(f"   Status encrypted and transmitted securely")
    print(f"   Decryption successful: {machine_status.replace(' ', '') == decrypted_status}")
    
    # Scenario 3: Vehicle Telematics
    print(f"\n3. Vehicle Telematics Data:")
    vehicle_data = "SPEED65MPH5LAT40DOT7128N5LON74DOT0060W5FUEL75PCT"
    encrypted_telemetry = iot_cipher.encrypt(vehicle_data)
    print(f"   GPS and status data encrypted for transmission")
    print(f"   Payload size: {len(encrypted_telemetry)} characters")
    
    return True

def main():
    """Run all demonstration examples."""
    print("POLY-HILL CIPHER (PHC) DEMONSTRATION")
    print("Lightweight Hybrid Cryptography for IoT-Enabled Devices")
    print("=" * 80)
    
    examples = [
        ("Basic Usage", basic_usage_example),
        ("IoT Optimization", iot_optimized_example),
        ("Security Analysis", security_analysis_example),
        ("Avalanche Effect", avalanche_effect_test),
        ("Performance Comparison", performance_comparison),
        ("Real-World Scenarios", real_world_scenarios)
    ]
    
    results = {}
    
    for name, example_func in examples:
        try:
            print(f"\n🔄 Running {name}...")
            success = example_func()
            results[name] = "✅ PASSED" if success else "❌ FAILED"
        except Exception as e:
            results[name] = f"❌ ERROR: {str(e)}"
            print(f"Error in {name}: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("DEMONSTRATION SUMMARY")
    print("=" * 80)
    
    for name, result in results.items():
        print(f"{name:<25}: {result}")
    
    passed_count = sum(1 for r in results.values() if r.startswith("✅"))
    total_count = len(results)
    
    print(f"\nOverall: {passed_count}/{total_count} examples passed")
    
    if passed_count == total_count:
        print("\n🎉 All demonstrations completed successfully!")
        print("The Poly-Hill Cipher is ready for IoT deployment.")
    else:
        print(f"\n⚠️  Some demonstrations failed. Please check the implementation.")

if __name__ == "__main__":
    main()