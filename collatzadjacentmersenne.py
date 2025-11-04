import matplotlib.pyplot as plt
import numpy as np

def mersenne_decomposition(n):
    """
    Decomposes n based on the largest Mersenne number less than or equal to n.
    """
    k = 0
    mersenne = 0
    while mersenne <= n:
        k += 1
        mersenne = (2**k) - 1
    k -= 1  # Adjust k to the largest Mersenne number *less* than n
    mersenne = (2**k) - 1
    q = n // mersenne
    r = n % mersenne
    return k, q, r

def collatz_sequence(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

# Example usage:
numbers = [7, 11, 27, 101, 341, 503, 126, 61]  # Example numbers
for n in numbers:
    k, q, r = mersenne_decomposition(n)
    sequence = collatz_sequence(n)

    print(f"Decomposition of {n}:")
    print(f"  k (for 2^k - 1): {k}")
    print(f"  q (quotient): {q}")
    print(f"  r (remainder): {r}")
    print(f"Collatz sequence length for {n}: {len(sequence)}")

    if r != 0:
        remainder_sequence = collatz_sequence(r)
        print(f"Collatz sequence length for remainder {r}: {len(remainder_sequence)}")
    else:
        print("Remainder is 0, skipping Collatz sequence for remainder.")
    print("-" * 20)