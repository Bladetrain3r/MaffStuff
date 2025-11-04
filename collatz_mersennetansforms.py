import matplotlib.pyplot as plt
import numpy as np

def is_mersenne(n):
    """Checks if a number is a Mersenne number (2^k - 1)."""
    if n <= 0:
        return False
    x = n + 1
    return (x & (x - 1)) == 0 and x != 0 # Efficiently checks if x is a power of 2

def mersenne_collatz_sequence(n, k, max_steps=100):  # Added max_steps parameter
    """
    Generates a Collatz-like sequence using a Mersenne-based transformation.

    Args:
        n: The starting number.
        k: The parameter defining the Mersenne numbers to use (2^k - 1 and 2^(k-1) - 1).
        max_steps: The maximum number of steps to generate.

    Returns:
        A list representing the sequence, and a boolean indicating if the sequence reached 1.
    """
    sequence = [n]
    for _ in range(max_steps):
        if n == 1:
            return sequence, True  # Reached 1 within the limit
        if n % 2 == 0:
            n //= 2
        else:
            n = (2**k - 1) * n + (2**(k-1) - 1)
        sequence.append(n)
    return sequence, False  # Did not reach 1 within the limit

# Test parameters
start_numbers = [3, 7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095, 8191, 341, 85]  # Mersenne numbers
k_values = [2, 3, 4, 5, 6, 7]  # Values of k for the transformation
max_steps = 1000

# Generate and analyze sequences
for n in start_numbers:
    print(f"Starting Number: {n} (Binary: {bin(n)[2:]})")
    for k in k_values:
        sequence, reached_one = mersenne_collatz_sequence(n, k, max_steps)
        if reached_one:
            print(f"  k={k}, Sequence Length: {len(sequence)}")
        else:
            print(f"  k={k}, Sequence Length: {len(sequence)} (Stubborn - did not reach 1 in {max_steps} steps)")
        #print(f"  Sequence: {sequence}") # Uncomment to see the actual sequences

    print("-" * 20)