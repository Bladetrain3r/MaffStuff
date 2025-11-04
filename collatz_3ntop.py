import matplotlib.pyplot as plt
import numpy as np
import collections
import math

def is_power_of_two(n):
    """Checks if a number is a power of two."""
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1

def collatz_sequence(n):
    """Generates the Collatz sequence for a given number n."""
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

def count_trailing_zeros(n):
    """Counts the number of trailing zeros in the binary representation of n."""
    binary_string = bin(n)[2:]
    count = 0
    for bit in reversed(binary_string):
        if bit == '0':
            count += 1
        else:
            break
    return count

def calculate_entropy(sequence):
  """Calculates the Shannon entropy of a sequence."""
  if not sequence:
    return 0  # Handle empty sequence case

  counts = collections.Counter(sequence)
  probabilities = [count / len(sequence) for count in counts.values()]
  entropy = -sum(p * math.log2(p) for p in probabilities if p > 0)
  return entropy

def get_representation(n, base):
    """Gets the representation of n in a given base."""
    if n == 0:
        return "0"

    digits = []
    while n > 0:
        digit = n % base
        if digit < 10:
            digits.insert(0, str(digit))
        else:
            digits.insert(0, chr(ord('A') + digit - 10))  # Use letters for digits >= 10
        n //= base
    return "".join(digits)

def analyze_entropy_across_bases(number, bases):
    """
    Analyzes the entropy of a number across different bases.
    """
    results = {}
    for base in bases:
        representation = get_representation(number, base)
        entropy = calculate_entropy(representation)
        max_entropy = math.log2(base) if base > 1 else 0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        results[base] = {
            'representation': representation,
            'entropy': entropy,
            'max_entropy': max_entropy,
            'normalized_entropy': normalized_entropy
        }
    return results

# Powers of two to test
powers = [2**i for i in range(1, 21)]

# Generate and analyze sequences
for power_of_two in powers:
    n = 3 * power_of_two + 1
    sequence = collatz_sequence(n)

    print(f"Power of Two: {power_of_two} (Binary: {bin(power_of_two)[2:]})")
    print(f"3n+1 Value: {n} (Binary: {bin(n)[2:]})")
    print(f"Sequence Length: {len(sequence)}")
    print(f"Maximum Value: {max(sequence)}")

    # Other analyses:
    trailing_zeros = [count_trailing_zeros(x) for x in sequence]
    print(f"Max Trailing Zeros: {max(trailing_zeros)}")

    # Entropy analysis
    bases_to_test = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    entropy_results = analyze_entropy_across_bases(n, bases_to_test)
    print("Entropy Across Bases:")
    for base, info in entropy_results.items():
        print(f"  Base {base}: Entropy = {info['entropy']:.3f}, Normalized = {info['normalized_entropy']:.3f}")

    print("-" * 20)