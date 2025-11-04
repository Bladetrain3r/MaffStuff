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

def calculate_slopes(sequence):
    """
    Calculates the cumulative effect of the positive and negative slopes 
    in logarithmic space for a given Collatz sequence.
    """
    log_sequence = np.log2(sequence)
    positive_slope = 0
    negative_slope = 0
    positive_slopes = []
    negative_slopes = []

    for i in range(len(sequence) - 1):
        if sequence[i] % 2 != 0:  # Odd number, 3n+1 step
            positive_slope += log_sequence[i+1] - log_sequence[i]
        else:  # Even number, n/2 step
            negative_slope += -1  # Each division by 2 contributes -1
        
        positive_slopes.append(positive_slope)
        negative_slopes.append(negative_slope)
    
    return positive_slopes, negative_slopes

def plot_slope_battle(sequence, start_number, label=None):
    """
    Plots the cumulative positive and negative slopes for a Collatz sequence.
    """
    positive_slopes, negative_slopes = calculate_slopes(sequence)
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(positive_slopes, label='Cumulative Positive Slope (3n+1)', color='red')
    plt.plot(negative_slopes, label='Cumulative Negative Slope (n/2)', color='blue')
    
    # Find the point where the negative slope surpasses the positive slope
    convergence_point = None
    for i in range(len(positive_slopes)):
        if negative_slopes[i] < positive_slopes[i]:
            convergence_point = i
            break

    if convergence_point is not None:
        plt.axvline(x=convergence_point, color='green', linestyle='--', label='Convergence Point')

    plt.xlabel("Step")
    plt.ylabel("Cumulative Slope (Logarithmic Space)")
    plt.title(f"Collatz Sequence Slope Battle for {start_number}{' (' + label + ')' if label else ''}")
    plt.legend()
    plt.grid(True)
    plt.show()

# Test numbers
# Test numbers
bit_limit_numbers = [3, 7, 15, 31, 63, 127, 255]
near_misses = [26, 27, 28, 55, 100, 126, 128, 129]
random_numbers = [101, 475, 682, 680, 1789, 503, 8738]
all_numbers = bit_limit_numbers + near_misses + random_numbers

# Analyze and plot for each number
for number in all_numbers:
    sequence = collatz_sequence(number)
    
    print(f"Number: {number} (Binary: {bin(number)[2:]})")
    print(f"Sequence Length: {len(sequence)}")
    print(f"Maximum Value: {max(sequence)}")
    
    trailing_zeros = [count_trailing_zeros(n) for n in sequence]
    print(f"Trailing Zeros: {trailing_zeros}")
    max_trailing_zeros = max(trailing_zeros)
    print(f"Maximum Trailing Zeros: {max_trailing_zeros}")
    # Generate slope battle plot
    is_bit_limit = number in bit_limit_numbers
    plot_slope_battle(sequence, number, label="Bit Limit - 1" if is_bit_limit else "Near Miss")
    
    print("-" * 20)

def is_near_miss_bl_minus_1(n):
    """
    Checks if a number is one less than a 'bit limit - 1' number.
    """
    # Check if n+1 is of the form 2^k - 1
    if (n + 1) & (n + 2) != 0:  # Efficiently checks if n+2 is a power of 2
        return False
      
    binary_string = bin(n)[2:]
    
    
    return all(bit == '1' for bit in binary_string[:-1]) and binary_string[-1] == '0'

# ... (other functions: collatz_sequence, etc.)

# Test near misses
test_numbers = [6, 14, 26, 28, 30, 62, 126]
for num in test_numbers:
    sequence = collatz_sequence(num)
    print(f"Sequence for {num} (Binary: {bin(num)[2:]}): {sequence}")
    if is_near_miss_bl_minus_1(num):
        print(f"{num} is one less than a BL-1 number.")
        print(f"It halves to: {num // 2}, which is a BL-1 number.")
    else:
        print(f"{num} is not one less than a BL-1 number.")
    print("-" * 20)