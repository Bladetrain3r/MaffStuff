import matplotlib.pyplot as plt
import numpy as np

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

def ends_with_101_zeros_corrected(n):
    """
    Checks if the binary representation of n ends with "101" 
    when preceded by any non-101 numbers, followed by one or more trailing zeros.
    """
    binary_string = bin(n)[2:]

    if len(binary_string) < 3:
        return False

    # Strip off trailing zeros
    zero_count = 0
    while binary_string.endswith('0'):
        binary_string = binary_string[:-1]
        zero_count += 1

    # Check if the remaining string ends with '101'
    if binary_string.endswith('101'):
        for bit in binary_string[-3::-1]:
          if bit == '1':
            return True
          elif bit == '0':
            continue
          else:
              return False
        return zero_count > 0
    else:
        return False

# Define the set S1 (numbers that eventually reach 5)
S1 = {5, 10, 20, 40, 80, 160, 320, 640}  # Add more powers of 2 times 5 as needed

# Test numbers
test_numbers = [5, 10, 20, 40, 21, 42, 84, 87381, 106, 53, 29, 301, 405, 503, 101, 475, 1789, 682, 680, 9, 27, 33, 48, 51]
for num in test_numbers:
    sequence = collatz_sequence(num)
    print(f"Sequence for {num} (Binary: {bin(num)[2:]}): {sequence}")
    if ends_with_101_zeros_corrected(num):
        print(f"{num} ends with '101' when preceded by a non-101 and followed by trailing zeros.")
    else:
        print(f"{num} does not end with '101' when preceded by a non-101 and followed by trailing zeros.")
    print("-" * 20)

# Plot the Collatz sequence for a specific number in binary
n = 27
sequence = collatz_sequence(n)
binary_sequence = [bin(num)[2:] for num in sequence]
print(f"Collatz sequence for {n}: {sequence}")
print(f"Binary sequence for {n}: {binary_sequence}")