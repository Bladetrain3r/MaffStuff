import matplotlib.pyplot as plt
import numpy as np

def generate_infinite_family_member(k):
    """Generates a member of the infinite family (2^(2k) - 1)/3."""
    return (2**(2*k) - 1) // 3

def is_power_of_two(n):
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1

def collatz_sequence(n):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

# Prepare data for plotting
ks = range(2, 129)
sequence_lengths = []

# Test the infinite family for k = 2 to 128
for k in ks:
    n = generate_infinite_family_member(k)
    sequence = collatz_sequence(n)
    sequence_lengths.append(len(sequence))
    print(f"k={k}, n={n}, Binary: {bin(n)[2:]}")
    print(f"Sequence: {sequence}")
    if is_power_of_two(sequence[1]):
        print(f"3n+1 = {sequence[1]} (Power of two)")
    else:
        print(f"Error: 3n+1 did not yield a power of two")
    print("-" * 20)

# Plot the results
slope, intercept = np.polyfit(ks, sequence_lengths, 1)
print(f"Slope: {slope}")
print(f"Intercept: {intercept}")
plt.plot(ks, sequence_lengths, label='Sequence Lengths')
plt.xlabel('k')
plt.ylabel('Sequence Length')
plt.title('Collatz Sequence Lengths for Infinite Family Members')
plt.legend()
plt.grid(True)
plt.show()