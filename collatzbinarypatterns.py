import matplotlib.pyplot as plt
import numpy as np

def generate_repeating_number(pattern, repetitions):
    """Generate a number from a repeating binary pattern"""
    binary = pattern * repetitions
    return int(binary, 2)

def collatz_sequence(n, max_steps=1000):
    """Generate Collatz sequence with safety limit"""
    sequence = [n]
    while n != 1 and len(sequence) < max_steps:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

def is_in_S1(n):
    while n % 2 == 0:
        n //= 2
    return n == 5


# Test patterns
patterns = {
    '110': 'Hybrid (110)',
    '111': 'All Ones',
    '101': 'L-type',
    '1100': 'Double Pair',
    '11000': 'Double-Triple Space'
}

# Create figure for multiple plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12))

# Plot growth with repetitions
repetitions = range(1, 6)
for pattern, label in patterns.items():
    values = [generate_repeating_number(pattern, r) for r in repetitions]
    ax1.plot(repetitions, values, marker='o', label=f'{label} ({pattern})')

ax1.set_xlabel('Number of Pattern Repetitions')
ax1.set_ylabel('Value')
ax1.set_title('Growth of Different Repeating Patterns')
ax1.grid(True)
ax1.legend()
ax1.set_yscale('log')

# Plot sequence lengths and maximum values
sequence_data = {}
for pattern, label in patterns.items():
    max_values = []
    lengths = []
    
    for r in repetitions:
        num = generate_repeating_number(pattern, r)
        sequence = collatz_sequence(num)
        max_values.append(max(sequence))
        lengths.append(len(sequence))
        
    sequence_data[pattern] = {
        'max_values': max_values,
        'lengths': lengths
    }

# Plot sequence lengths
for pattern, label in patterns.items():
    ax2.plot(repetitions, sequence_data[pattern]['lengths'], 
             marker='o', linestyle='-', label=f'{label} Length')

ax2.set_xlabel('Number of Pattern Repetitions')
ax2.set_ylabel('Sequence Length to Reach 1')
ax2.set_title('Collatz Sequence Lengths for Different Patterns')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.show()

def contains_pattern(n, pattern):
    """Checks if the binary representation of n contains the given pattern."""
    binary_string = bin(n)[2:]
    return pattern in binary_string

def is_in_set(n, target_set):
    """Checks if a number belongs to a given set."""
    return n in target_set

def collatz_sequence_optimized(n, target_set, pattern=None):
    """
    Generates the Collatz sequence for a given number n, stopping early 
    if a number in the target_set or a number with the specified pattern is found.
    """
    sequence = [n]
    while n != 1:
        if n in target_set or (pattern and contains_pattern(n, pattern)):
            return sequence  # Stop early if target or pattern is found

        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

# Define the set S1 (numbers that eventually reach 5)
S1 = {5, 10, 20, 40, 80, 160, 320, 640}  # Add more powers of 2 times 5 as needed

# Test numbers with and without the "101" pattern
test_numbers = [6, 15, 27, 53, 106, 89, 115, 213, 87381]  # Add more numbers
for num in test_numbers:
    sequence = collatz_sequence_optimized(num, S1, "101")
    print(f"Sequence for {num} (Binary: {bin(num)[2:]}): {sequence}")
    if contains_pattern(num, "101"):
        print(f"{num} contains the '101' pattern.")
    else:
        print(f"{num} does not contain the '101' pattern.")
    
    if any(is_in_set(s, S1) for s in sequence):
        print(f"{num} reaches S1.")
    else:
        print(f"{num} does not reach S1 (within the observed sequence).")

    print("-" * 20)
# Print detailed statistics
print("\nDetailed Pattern Analysis:")
print("-" * 60)
for pattern, label in patterns.items():
    print(f"\n{label} ({pattern}):")
    for r in repetitions:
        num = generate_repeating_number(pattern, r)
        sequence = collatz_sequence(num)
        print(f"{r} repetitions:")
        print(f"  Starting value: {num}")
        print(f"  Binary: {bin(num)[2:]}")
        print(f"  Sequence length: {len(sequence)}")
        print(f"  Max value: {max(sequence)}")
        growth_rate = max(sequence) / num if num > 0 else 0
        print(f"  Growth rate: {growth_rate:.2f}x")