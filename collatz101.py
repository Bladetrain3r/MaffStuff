import matplotlib.pyplot as plt
import numpy as np

def contains_pattern(n, pattern):
    """Checks if the binary representation of n contains the given pattern."""
    binary_string = bin(n)[2:]
    return pattern in binary_string

def is_in_S1(n):
    """Checks if a number belongs to the secondary harbor set S1."""
    while n % 2 == 0:
        n //= 2
    return n == 5

def collatz_sequence_to_power_of_two(n):
    """
    Generates the Collatz sequence for a given number n until a power of two is reached.
    Returns the sequence and the number of steps to reach the power of two.
    """
    sequence = [n]
    steps = 0
    while not is_power_of_two(n):
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
        steps += 1
    return sequence, steps

def is_power_of_two(n):
    """Checks if a number is a power of two."""
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1

def collatz_sequence_full(n):
    """
    Generates the full Collatz sequence for a given number n, 
    regardless of whether it hits S1 or matches a pattern.
    """
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

# Define the set S1 (numbers that eventually reach 5)
S1 = {5, 10, 20, 40, 80, 160, 320, 640}  # Add more powers of 2 times 5 as needed

# Test numbers with and without the "101" pattern
# test_numbers = [6, 9, 19, 15, 27, 53, 106, 89, 115, 213, 87381]  # Add more numbers

np.random.seed(0)  # For reproducibility
test_numbers = np.random.randint(1, 1000, size=10)

for num in test_numbers:
    sequence = collatz_sequence_full(num)  # Generate full sequence
    
    print(f"Sequence for {num} (Binary: {bin(num)[2:]}): {sequence}")
    
    has_101 = contains_pattern(num, "101")
    reaches_S1 = any(is_in_S1(s) for s in sequence)
    
    if has_101:
        print(f"{num} contains the '101' pattern.")
    else:
        print(f"{num} does not contain the '101' pattern.")
    
    if reaches_S1:
        print(f"{num} reaches S1.")
    else:
        print(f"{num} does not reach S1 (within the observed sequence).")

    print("-" * 20)

for i in range(1, 300):
    sequence, steps = collatz_sequence_to_power_of_two(i)
    if steps > 1:
        print(f"Number: {i}, Steps to reach a power of two: {steps}")