import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple, Dict
import math

class CollatzAnalyzer:
    def __init__(self, max_k: int = 50):
        self.max_k = max_k
        self.l_harbors = {}
        self.sequences = {}
        
    def generate_l_harbor(self, k: int) -> int:
        """Generate the kth L-type harbor: (2^(2k) - 1)/3"""
        return (2**(2*k) - 1) // 3
    
    def get_binary_rep(self, n: int) -> str:
        """Get binary representation of a number"""
        return bin(n)[2:]  # Remove '0b' prefix
    
    def get_prime_factors(self, n: int) -> List[int]:
        """Get prime factorization of a number"""
        factors = []
        num = n
        
        for i in range(2, int(math.sqrt(num)) + 1):
            while num % i == 0:
                factors.append(i)
                num //= i
        
        if num > 1:
            factors.append(num)
            
        return factors
    
    def collatz_sequence(self, n: int) -> List[int]:
        """Generate Collatz sequence for a number"""
        sequence = [n]
        while n != 1:
            if n % 2 == 0:
                n //= 2
            else:
                n = 3 * n + 1
            sequence.append(n)
        return sequence
    
    def analyze_l_harbors(self):
        """Analyze L-type harbors up to max_k"""
        for k in range(2, self.max_k + 1):
            harbor = self.generate_l_harbor(k)
            binary = self.get_binary_rep(harbor)
            factors = self.get_prime_factors(harbor)
            sequence = self.collatz_sequence(harbor)
            
            self.l_harbors[k] = {
                'value': harbor,
                'binary': binary,
                'factors': factors,
                'sequence_length': len(sequence),
                'sequence': sequence
            }
    
    def plot_sequence_lengths(self):
        """Plot sequence lengths against k"""
        k_values = list(self.l_harbors.keys())
        lengths = [data['sequence_length'] for data in self.l_harbors.values()]
        
        plt.figure(figsize=(12, 6))
        plt.plot(k_values, lengths, 'b-', label='Actual Length')
        
        # Plot theoretical 2k + 2 line
        theoretical = [2*k + 2 for k in k_values]
        plt.plot(k_values, theoretical, 'r--', label='Theoretical (2k + 2)')
        
        plt.xlabel('k')
        plt.ylabel('Sequence Length')
        plt.title('L-harbor Sequence Lengths')
        plt.legend()
        plt.grid(True)
        plt.show()
    
    def print_analysis(self):
        """Print detailed analysis of L-harbors"""
        print("\nL-harbor Analysis:")
        print("k\tValue\tBinary\tFactors\tSeq Length")
        print("-" * 60)
        
        for k, data in self.l_harbors.items():
            print(f"{k}\t{data['value']}\t{data['binary']}\t{data['factors']}\t{data['sequence_length']}")

# Example usage
def main():
    analyzer = CollatzAnalyzer(max_k=20)  # Analyze up to L(20)
    analyzer.analyze_l_harbors()
    analyzer.print_analysis()
    analyzer.plot_sequence_lengths()
    
    # Additional analysis of specific prime products
    def analyze_prime_product(primes: List[int]):
        n = math.prod(primes)
        binary = bin(n)[2:]
        sequence = analyzer.collatz_sequence(n)
        print(f"\nAnalyzing product of primes {primes}:")
        print(f"Number: {n}")
        print(f"Binary: {binary}")
        print(f"Sequence length: {len(sequence)}")
        print(f"First few steps: {sequence[:5]}...")
    
    # Test some prime products
    test_cases = [
        [3, 5],
        [3, 7],
        [3, 11],
        [5, 7],
        [5, 11],
        [7, 11]
    ]
    
    for primes in test_cases:
        analyze_prime_product(primes)

if __name__ == "__main__":
    main()