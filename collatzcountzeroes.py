from random import randint as randy
import matplotlib.pyplot as plt
import numpy as np


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

def plot_trailing_zeros(sequence, start_number):
    """Plots the number of trailing zeros at each step of the Collatz sequence."""
    trailing_zeros = [count_trailing_zeros(n) for n in sequence]

    plt.figure(figsize=(10, 6))
    plt.plot(trailing_zeros, marker='o', linestyle='-')
    plt.xlabel("Step")
    plt.ylabel("Number of Trailing Zeros")
    plt.title(f"Trailing Zeros in Collatz Sequence for {start_number}")
    plt.grid(True)
    plt.show()

def plot_trailing_zeros_and_binary(sequence, start_number):
    """Plots trailing zeros and binary representations for a Collatz sequence."""
    trailing_zeros = [count_trailing_zeros(n) for n in sequence]
    binary_reps = [bin(n)[2:] for n in sequence]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    # Plot trailing zeros
    ax1.plot(trailing_zeros, marker='o', linestyle='-')
    ax1.set_ylabel("Number of Trailing Zeros")
    ax1.set_title(f"Trailing Zeros and Binary Representation for {start_number}")
    ax1.grid(True)

    # Plot binary representations
    y_values = list(range(len(sequence)))
    for i, binary_string in enumerate(binary_reps):
        ax2.text(i, 0, binary_string, ha='center', va='bottom', rotation='vertical')

    ax2.set_xlabel("Step")
    ax2.set_ylabel("Binary Representation")
    ax2.set_yticks([])  # Hide y-ticks for binary representation
    ax2.grid(True)

    plt.tight_layout()
    plt.show()
    
def plot_trailing_zeros_comparison(sequences, start_numbers):
    """
    Plots the number of trailing zeros for multiple Collatz sequences on the same graph,
    along with a moving average and slope calculations.
    """
    plt.figure(figsize=(10, 6))
    for i, sequence in enumerate(sequences):
        trailing_zeros = [count_trailing_zeros(n) for n in sequence]
        plt.plot(trailing_zeros, marker='o', linestyle='-', label=f"{start_numbers[i]}", alpha=0.7)

        # Calculate and plot moving average
        window_size = 15  # Adjust window size as needed
        moving_avg = np.convolve(trailing_zeros, np.ones(window_size), 'valid') / window_size
        plt.plot(range(window_size - 1, len(trailing_zeros)), moving_avg, linestyle='--', linewidth=2, color='k')

        # Calculate and print slopes for the last portion of the moving average
        if len(moving_avg) > 10: # Ensure enough data points for slope calculation
            slope = np.polyfit(range(len(moving_avg) - 10, len(moving_avg)), moving_avg[-10:], 1)[0]
            print(f"Slope of moving average for {start_numbers[i]} (last 10 points): {slope:.4f}")

    plt.xlabel("Step")
    plt.ylabel("Number of Trailing Zeros")
    plt.title("Comparison of Trailing Zeros in Collatz Sequences")
    plt.legend()
    plt.grid(True)
    plt.show()


# Example usage:
start_numbers = [27, 31, 41, 55, 123, 45, 61, 51]  # Example start numbers

# Individual plots with binary representation
for number in start_numbers:
  sequence = collatz_sequence(number)
  plot_trailing_zeros_and_binary(sequence, number)

# Comparison plot
sequences = [collatz_sequence(number) for number in start_numbers]
plot_trailing_zeros_comparison(sequences, start_numbers)

# Example usage:
number = randy(1, 1000)  # Or any other number you want to test
sequence = collatz_sequence(number)
plot_trailing_zeros(sequence, number)