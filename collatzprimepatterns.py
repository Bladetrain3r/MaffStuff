import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
from typing import List, Tuple

def collatz_sequence(n: int) -> List[int]:
    """Generate Collatz sequence for a number"""
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

def analyze_binary_pattern(n: int) -> dict:
    """Analyze binary representation patterns"""
    binary = bin(n)[2:]  # Remove '0b' prefix
    pattern_info = {
        'binary': binary,
        'length': len(binary),
        'ones': binary.count('1'),
        'zeros': binary.count('0'),
        'has_alternating_pattern': all(binary[i:i+2] == '10' for i in range(0, len(binary)-1, 2)),
        'starts_with_1': binary.startswith('1'),
        'ends_with_1': binary.endswith('1')
    }
    return pattern_info

def analyze_prime_product(primes: List[int]) -> dict:
    """Analyze properties of product of primes"""
    n = np.prod(primes)
    sequence = collatz_sequence(n)
    binary_analysis = analyze_binary_pattern(n)
    
    # Find first power of 2 in sequence (if any)
    first_power_2 = next((x for x in sequence if (x & (x-1) == 0)), None)
    steps_to_power_2 = sequence.index(first_power_2) if first_power_2 else None
    
    return {
        'number': n,
        'primes': primes,
        'sequence_length': len(sequence),
        'first_power_2': first_power_2,
        'steps_to_power_2': steps_to_power_2,
        'binary_analysis': binary_analysis
    }

def main():
    # Generate first few primes
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(np.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    primes = [p for p in range(2, 20) if is_prime(p)]
    
    # Test different combinations of 2 and 3 primes
    results = []
    
    # Test pairs of primes
    print("Analyzing pairs of primes:")
    for combo in combinations(primes, 2):
        result = analyze_prime_product(list(combo))
        results.append(result)
        print(f"\nPrimes: {combo}")
        print(f"Number: {result['number']}")
        print(f"Binary: {result['binary_analysis']['binary']}")
        print(f"Sequence length: {result['sequence_length']}")
        print(f"Steps to first power of 2: {result['steps_to_power_2']}")
        print(f"Alternating pattern? {result['binary_analysis']['has_alternating_pattern']}")
    
    # Test triplets of primes
    print("\nAnalyzing triplets of primes:")
    for combo in combinations(primes, 3):
        result = analyze_prime_product(list(combo))
        results.append(result)
        print(f"\nPrimes: {combo}")
        print(f"Number: {result['number']}")
        print(f"Binary: {result['binary_analysis']['binary']}")
        print(f"Sequence length: {result['sequence_length']}")
        print(f"Steps to first power of 2: {result['steps_to_power_2']}")
        print(f"Alternating pattern? {result['binary_analysis']['has_alternating_pattern']}")
    
    # Plot relationship between number of 1s in binary and sequence length
    plt.figure(figsize=(10, 6))
    ones_counts = [r['binary_analysis']['ones'] for r in results]
    seq_lengths = [r['sequence_length'] for r in results]
    plt.scatter(ones_counts, seq_lengths, alpha=0.6)
    plt.xlabel('Number of 1s in binary representation')
    plt.ylabel('Sequence Length')
    plt.title('Relationship between Binary 1s and Sequence Length')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()