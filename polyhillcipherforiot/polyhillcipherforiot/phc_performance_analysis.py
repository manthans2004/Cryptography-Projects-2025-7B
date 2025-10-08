"""
Performance Analysis Tools for Poly-Hill Cipher

This module provides comprehensive performance analysis and benchmarking
tools for evaluating the PHC algorithm in IoT environments.

Author: Cryptography Implementation
Date: September 2025
"""

import time
import psutil
import os
import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple, Optional
import json
from datetime import datetime
from poly_hill_cipher import PolyHillCipher, IoTPolyHillCipher

class PHCPerformanceAnalyzer:
    """Comprehensive performance analysis tools for Poly-Hill Cipher."""
    
    def __init__(self):
        self.results = {}
        self.benchmarks = []
    
    def measure_execution_time(self, cipher, text: str, iterations: int = 1000) -> Dict[str, float]:
        """
        Measure encryption and decryption execution times.
        
        Args:
            cipher: PHC cipher instance.
            text (str): Test text.
            iterations (int): Number of iterations for averaging.
            
        Returns:
            Dict[str, float]: Timing measurements in milliseconds.
        """
        # Warm-up runs
        for _ in range(10):
            encrypted = cipher.encrypt(text)
            cipher.decrypt(encrypted)
        
        # Measure encryption time
        start_time = time.perf_counter()
        encrypted_texts = []
        for _ in range(iterations):
            encrypted = cipher.encrypt(text)
            encrypted_texts.append(encrypted)
        encryption_time = (time.perf_counter() - start_time) * 1000  # Convert to ms
        
        # Measure decryption time
        start_time = time.perf_counter()
        for encrypted in encrypted_texts:
            cipher.decrypt(encrypted)
        decryption_time = (time.perf_counter() - start_time) * 1000
        
        return {
            'encryption_time_ms': encryption_time,
            'decryption_time_ms': decryption_time,
            'avg_encryption_ms': encryption_time / iterations,
            'avg_decryption_ms': decryption_time / iterations,
            'total_time_ms': encryption_time + decryption_time,
            'throughput_chars_per_sec': len(text) * iterations / ((encryption_time + decryption_time) / 1000)
        }
    
    def measure_memory_usage(self, cipher, text: str) -> Dict[str, float]:
        """
        Measure memory usage during cipher operations.
        
        Args:
            cipher: PHC cipher instance.
            text (str): Test text.
            
        Returns:
            Dict[str, float]: Memory usage measurements in bytes.
        """
        process = psutil.Process(os.getpid())
        
        # Baseline memory
        baseline_memory = process.memory_info().rss
        
        # Memory after key generation
        cipher.generate_key()
        key_memory = process.memory_info().rss
        
        # Memory during encryption
        encrypted = cipher.encrypt(text)
        encryption_memory = process.memory_info().rss
        
        # Memory during decryption
        decrypted = cipher.decrypt(encrypted)
        decryption_memory = process.memory_info().rss
        
        return {
            'baseline_memory_bytes': baseline_memory,
            'key_generation_overhead_bytes': key_memory - baseline_memory,
            'encryption_memory_bytes': encryption_memory,
            'decryption_memory_bytes': decryption_memory,
            'peak_memory_overhead_bytes': max(encryption_memory, decryption_memory) - baseline_memory,
            'memory_efficiency_bytes_per_char': (encryption_memory - baseline_memory) / len(text) if len(text) > 0 else 0
        }
    
    def scalability_analysis(self, cipher_class, text_sizes: List[int], block_sizes: List[int]) -> Dict:
        """
        Analyze how performance scales with text size and block size.
        
        Args:
            cipher_class: PHC cipher class.
            text_sizes (List[int]): Different text sizes to test.
            block_sizes (List[int]): Different block sizes to test.
            
        Returns:
            Dict: Scalability analysis results.
        """
        results = {
            'text_size_scaling': {},
            'block_size_scaling': {}
        }
        
        # Test text size scaling (fixed block size)
        base_text = "A" * 100  # Base pattern
        for size in text_sizes:
            test_text = (base_text * (size // len(base_text) + 1))[:size]
            cipher = cipher_class(block_size=3)
            cipher.generate_key(seed=12345)
            
            timing = self.measure_execution_time(cipher, test_text, iterations=100)
            memory = self.measure_memory_usage(cipher, test_text)
            
            results['text_size_scaling'][size] = {
                'avg_encryption_ms': timing['avg_encryption_ms'],
                'avg_decryption_ms': timing['avg_decryption_ms'],
                'memory_overhead': memory['peak_memory_overhead_bytes'],
                'throughput': timing['throughput_chars_per_sec']
            }
        
        # Test block size scaling (fixed text size)
        test_text = "PERFORMANCE ANALYSIS FOR DIFFERENT BLOCK SIZES" * 10
        for block_size in block_sizes:
            try:
                cipher = cipher_class(block_size=block_size)
                cipher.generate_key(seed=12345)
                
                timing = self.measure_execution_time(cipher, test_text, iterations=100)
                memory = self.measure_memory_usage(cipher, test_text)
                
                results['block_size_scaling'][block_size] = {
                    'avg_encryption_ms': timing['avg_encryption_ms'],
                    'avg_decryption_ms': timing['avg_decryption_ms'],
                    'memory_overhead': memory['peak_memory_overhead_bytes'],
                    'throughput': timing['throughput_chars_per_sec']
                }
            except Exception as e:
                results['block_size_scaling'][block_size] = {'error': str(e)}
        
        return results
    
    def iot_device_simulation(self, cipher, scenarios: List[Dict]) -> Dict:
        """
        Simulate PHC performance on different IoT device classes.
        
        Args:
            cipher: PHC cipher instance.
            scenarios (List[Dict]): IoT device scenarios to test.
            
        Returns:
            Dict: IoT simulation results.
        """
        results = {}
        
        for scenario in scenarios:
            device_name = scenario['device_name']
            cpu_limit = scenario.get('cpu_mhz', 1000)
            memory_limit = scenario.get('memory_kb', 1024)
            typical_payload = scenario.get('payload', "SENSOR DATA")
            
            # Simulate limited processing by introducing delays
            processing_factor = 1000 / cpu_limit  # Normalize to 1000 MHz baseline
            
            start_time = time.perf_counter()
            
            # Simulate key generation overhead
            cipher.generate_key()
            key_gen_time = (time.perf_counter() - start_time) * processing_factor * 1000
            
            # Measure encryption/decryption with processing simulation
            timing = self.measure_execution_time(cipher, typical_payload, iterations=10)
            simulated_encryption_time = timing['avg_encryption_ms'] * processing_factor
            simulated_decryption_time = timing['avg_decryption_ms'] * processing_factor
            
            # Check memory constraints
            memory_usage = self.measure_memory_usage(cipher, typical_payload)
            memory_usage_kb = memory_usage['peak_memory_overhead_bytes'] / 1024
            memory_feasible = memory_usage_kb <= memory_limit
            
            # Energy estimation (simplified model)
            # Assume 1 mW per MHz and operation time
            energy_mwh = (cpu_limit / 1000) * (simulated_encryption_time + simulated_decryption_time) / 3600
            
            results[device_name] = {
                'key_generation_time_ms': key_gen_time,
                'encryption_time_ms': simulated_encryption_time,
                'decryption_time_ms': simulated_decryption_time,
                'memory_usage_kb': memory_usage_kb,
                'memory_feasible': memory_feasible,
                'estimated_energy_mwh': energy_mwh,
                'performance_rating': self._calculate_iot_rating(
                    simulated_encryption_time + simulated_decryption_time,
                    memory_feasible,
                    energy_mwh
                )
            }
        
        return results
    
    def _calculate_iot_rating(self, total_time_ms: float, memory_ok: bool, energy_mwh: float) -> str:
        """Calculate performance rating for IoT suitability."""
        if not memory_ok:
            return "Poor - Memory Exceeded"
        elif total_time_ms > 1000:  # > 1 second
            return "Poor - Too Slow"
        elif total_time_ms > 100:  # > 100ms
            return "Fair - Acceptable"
        elif total_time_ms > 10:  # > 10ms
            return "Good - Fast"
        else:
            return "Excellent - Very Fast"
    
    def comparative_analysis(self, cipher_configs: List[Dict], test_text: str) -> Dict:
        """
        Compare different cipher configurations.
        
        Args:
            cipher_configs (List[Dict]): Different cipher configurations to test.
            test_text (str): Common test text.
            
        Returns:
            Dict: Comparative analysis results.
        """
        results = {}
        
        for config in cipher_configs:
            config_name = config['name']
            cipher_class = config['cipher_class']
            block_size = config.get('block_size', 3)
            modulus = config.get('modulus', 26)
            
            try:
                cipher = cipher_class(block_size=block_size, modulus=modulus)
                cipher.generate_key(seed=12345)  # Fixed seed for fair comparison
                
                timing = self.measure_execution_time(cipher, test_text, iterations=500)
                memory = self.measure_memory_usage(cipher, test_text)
                
                # Test correctness
                encrypted = cipher.encrypt(test_text)
                decrypted = cipher.decrypt(encrypted)
                correctness = test_text.replace(" ", "") == decrypted
                
                results[config_name] = {
                    'timing': timing,
                    'memory': memory,
                    'correctness': correctness,
                    'config': {
                        'block_size': block_size,
                        'modulus': modulus,
                        'cipher_type': cipher_class.__name__
                    }
                }
            except Exception as e:
                results[config_name] = {'error': str(e)}
        
        return results
    
    def generate_performance_report(self, analysis_results: Dict, output_file: str = None) -> str:
        """
        Generate a comprehensive performance report.
        
        Args:
            analysis_results (Dict): Results from various analyses.
            output_file (str): Optional file to save the report.
            
        Returns:
            str: Formatted performance report.
        """
        report = []
        report.append("="*80)
        report.append("POLY-HILL CIPHER PERFORMANCE ANALYSIS REPORT")
        report.append("="*80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Executive Summary
        report.append("EXECUTIVE SUMMARY")
        report.append("-"*40)
        if 'comparative' in analysis_results:
            best_config = min(analysis_results['comparative'].items(), 
                             key=lambda x: x[1].get('timing', {}).get('avg_encryption_ms', float('inf')))
            report.append(f"Best performing configuration: {best_config[0]}")
            report.append(f"Average encryption time: {best_config[1]['timing']['avg_encryption_ms']:.2f}ms")
        report.append("")
        
        # Detailed Results
        for analysis_type, results in analysis_results.items():
            report.append(f"{analysis_type.upper()} ANALYSIS")
            report.append("-"*40)
            
            if analysis_type == 'scalability':
                report.append("Text Size Scaling:")
                for size, metrics in results.get('text_size_scaling', {}).items():
                    report.append(f"  {size} chars: {metrics['avg_encryption_ms']:.2f}ms encryption")
                
                report.append("Block Size Scaling:")
                for block_size, metrics in results.get('block_size_scaling', {}).items():
                    if 'error' not in metrics:
                        report.append(f"  Block {block_size}: {metrics['avg_encryption_ms']:.2f}ms encryption")
            
            elif analysis_type == 'iot_simulation':
                for device, metrics in results.items():
                    report.append(f"  {device}:")
                    report.append(f"    Performance: {metrics['performance_rating']}")
                    report.append(f"    Encryption: {metrics['encryption_time_ms']:.2f}ms")
                    report.append(f"    Memory: {metrics['memory_usage_kb']:.1f}KB")
            
            elif analysis_type == 'comparative':
                for config, metrics in results.items():
                    if 'error' not in metrics:
                        report.append(f"  {config}:")
                        report.append(f"    Encryption: {metrics['timing']['avg_encryption_ms']:.2f}ms")
                        report.append(f"    Memory overhead: {metrics['memory']['peak_memory_overhead_bytes']/1024:.1f}KB")
                        report.append(f"    Correctness: {metrics['correctness']}")
            
            report.append("")
        
        report_text = "\n".join(report)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
        
        return report_text
    
    def benchmark_suite(self) -> Dict:
        """
        Run comprehensive benchmark suite.
        
        Returns:
            Dict: Complete benchmark results.
        """
        print("Running comprehensive PHC benchmark suite...")
        
        # Test configurations
        cipher_configs = [
            {'name': 'Standard_3x3', 'cipher_class': PolyHillCipher, 'block_size': 3},
            {'name': 'Standard_2x2', 'cipher_class': PolyHillCipher, 'block_size': 2},
            {'name': 'IoT_2x2', 'cipher_class': IoTPolyHillCipher, 'block_size': 2},
        ]
        
        # IoT device scenarios
        iot_scenarios = [
            {'device_name': 'Arduino_Nano', 'cpu_mhz': 16, 'memory_kb': 32, 'payload': 'TEMP25HUM60'},
            {'device_name': 'ESP32', 'cpu_mhz': 240, 'memory_kb': 320, 'payload': 'SENSOR DATA PAYLOAD'},
            {'device_name': 'Raspberry_Pi_Zero', 'cpu_mhz': 1000, 'memory_kb': 512000, 'payload': 'EXTENDED TELEMETRY DATA'},
        ]
        
        test_text = "PERFORMANCE BENCHMARKING FOR IOT CRYPTOGRAPHY SYSTEMS"
        
        results = {}
        
        # Comparative analysis
        print("  Running comparative analysis...")
        results['comparative'] = self.comparative_analysis(cipher_configs, test_text)
        
        # Scalability analysis
        print("  Running scalability analysis...")
        results['scalability'] = self.scalability_analysis(
            PolyHillCipher,
            text_sizes=[50, 100, 200, 500, 1000],
            block_sizes=[2, 3, 4]
        )
        
        # IoT simulation
        print("  Running IoT device simulation...")
        iot_cipher = IoTPolyHillCipher(block_size=2)
        results['iot_simulation'] = self.iot_device_simulation(iot_cipher, iot_scenarios)
        
        return results

def main():
    """Run performance analysis demonstration."""
    analyzer = PHCPerformanceAnalyzer()
    
    print("PHC Performance Analysis Tool")
    print("="*50)
    
    # Run benchmark suite
    results = analyzer.benchmark_suite()
    
    # Generate report
    print("\nGenerating performance report...")
    report = analyzer.generate_performance_report(
        results, 
        output_file="phc_performance_report.txt"
    )
    
    print("\nPerformance Analysis Complete!")
    print("Report saved to: phc_performance_report.txt")
    print("\nKey Findings Summary:")
    print("-"*30)
    
    # Extract key findings
    if 'comparative' in results:
        fastest_config = min(
            results['comparative'].items(),
            key=lambda x: x[1].get('timing', {}).get('avg_encryption_ms', float('inf')),
            default=("None", {})
        )
        if fastest_config[1]:
            print(f"Fastest configuration: {fastest_config[0]}")
            print(f"Encryption time: {fastest_config[1]['timing']['avg_encryption_ms']:.2f}ms")
    
    if 'iot_simulation' in results:
        suitable_devices = [device for device, metrics in results['iot_simulation'].items() 
                          if 'Good' in metrics.get('performance_rating', '') or 'Excellent' in metrics.get('performance_rating', '')]
        print(f"IoT devices with good performance: {', '.join(suitable_devices)}")
    
    return results

if __name__ == "__main__":
    main()