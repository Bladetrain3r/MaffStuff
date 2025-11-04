import math
import collections
import numpy as np

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

# Example usage
bases_to_test = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
numbers_to_analyze = [327, 255, 511, 85, 341] # P, M, and L types

for number in numbers_to_analyze:
  print(f"Entropy Analysis Across Bases for {number}")
  results = analyze_entropy_across_bases(number, bases_to_test)

  print("-" * 50)
  print(f"Number: {number}")
  for base, info in results.items():
      print(f"Base: {base}")
      print(f"  Representation: {info['representation']}")
      print(f"  Entropy: {info['entropy']:.3f}")
      print(f"  Max Possible Entropy: {info['max_entropy']:.3f}")
      print(f"  Normalized Entropy: {info['normalized_entropy']:.3f}")
  print("-" * 50)