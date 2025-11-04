import matplotlib.pyplot as plt
import numpy as np

def is_mersenne(n):
    """Checks if a number is a Mersenne number (2^k - 1)."""
    if n <= 0:
        return False
    x = n + 1
    return (x & (x - 1)) == 0 and x != 0 # Efficiently checks if x is a power of 2

def mersenne_collatz_sequence_modified(n, k, max_steps=100, halving_rule='k'):
    """
    Generates a Collatz-like sequence using a Mersenne-based transformation with a modified halving rule.

    Args:
        n: The starting number.
        k: The parameter defining the Mersenne numbers to use (2^k - 1 and 2^(k-1) - 1).
        max_steps: The maximum number of steps to generate.
        halving_rule:  
            'k': Divides by 2^k when n is divisible by 2^k.
            'k-1': Divides by 2^(k-1) when n is divisible by 2^(k-1).
            'standard': Standard n/2 halving rule

    Returns:
        A list representing the sequence, and a boolean indicating if the sequence reached 1.
    """
    sequence = [n]
    for _ in range(max_steps):
        if n == 1:
            return sequence, True
        
        if halving_rule == 'k' and n % (2**k) == 0:
            n //= (2**k)
        elif halving_rule == 'k-1' and n % (2**(k-1)) == 0:
            n //= (2**(k-1))
        elif halving_rule == 'n/4' and n % 4 == 0:
            n //= 4
        elif halving_rule == 'n/8' and n % 8 == 0:
            n //= 8
        elif halving_rule == 'n/16' and n % 16 == 0:
            n //= 16
        elif n % 2 == 0:
            n //= 2
        else:
            n = (2**k - 1) * n + (2**(k-1) - 1)
        
        sequence.append(n)
    return sequence, False

# Test parameters
start_numbers = [3, 7, 15, 31, 63, 127, 255, 511, 1023, 341, 85]  # Mersenne numbers and a few prime harbors
k_values = [2, 3, 4, 5, 6]  # Values of k for the transformation
max_steps = 1000
halving_rules = ['standard', 'k', 'k-1', 'n/4', 'n/8', 'n/16'] # Different halving rules to test

# Generate and analyze sequences
for n in start_numbers:
    print(f"Starting Number: {n} (Binary: {bin(n)[2:]})")
    for k in k_values:
        for halving_rule in halving_rules:
            sequence, reached_one = mersenne_collatz_sequence_modified(n, k, max_steps, halving_rule)
            if reached_one:
                print(f"  k={k}, Halving Rule: {halving_rule}, Sequence Length: {len(sequence)}")
            else:
                print(f"  k={k}, Halving Rule: {halving_rule}, Sequence Length: {len(sequence)} (Stubborn - did not reach 1 in {max_steps} steps)")
    print("-" * 20)