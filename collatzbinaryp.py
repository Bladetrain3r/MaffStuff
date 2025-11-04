import matplotlib.pyplot as plt

def binary_collatz_sequence(n):
    """
    Generates the Collatz sequence for a given number n, 
    representing numbers in binary.

    Args:
        n: The starting number (an integer).

    Returns:
        A list of binary strings representing the Collatz sequence.
    """
    sequence = [bin(n)[2:]]  # Store sequence as binary strings
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(bin(n)[2:])
    return sequence

def contains_101_pattern(n):
    """Checks if the binary representation of n contains the '101' pattern."""
    binary_string = bin(n)[2:]
    return "101" in binary_string

def plot_binary_sequence(sequence):
    """
    Plots the binary sequence, highlighting changes caused by 3n+1.

    Args:
        sequence: A list of binary strings representing the Collatz sequence.
    """
    y_values = list(range(len(sequence)))

    plt.figure(figsize=(15, 5))
    for i, binary_string in enumerate(sequence):
        if i > 0:
            # Check if the previous step was 3n+1
            if int(sequence[i-1], 2) % 2 != 0:
                plt.plot(i, int(binary_string, 2), 'ro')  # Red dot for 3n+1
            else:
                plt.plot(i, int(binary_string, 2), 'bo')  # Blue dot for n/2
        else:
            plt.plot(i, int(binary_string, 2), 'go')  # Green dot for the start

        plt.text(i, int(binary_string, 2), binary_string, ha='center', va='bottom')

    plt.plot(y_values, [int(s, 2) for s in sequence], 'k-', linewidth=0.5)  # Thin line connecting points

    plt.xlabel("Step")
    plt.ylabel("Value (Decimal)")
    plt.title("Collatz Sequence in Binary")
    plt.grid(True)
    plt.show()

# Example usage:
start_number = 341 # or 27 or any other number you want to test
sequence = binary_collatz_sequence(start_number)
plot_binary_sequence(sequence)
start_numbers = [27, 341, 15, 21, 7, 19, 3245, 34]  # Add more start numbers as needed

plt.figure(figsize=(15, 5))

import numpy as np


def plot_binary_sequence_log(sequence, start_number):
    """
    Plots the binary sequence on a logarithmic scale.
    """
    y_values = list(range(len(sequence)))

    plt.figure(figsize=(10, 5))
    
    for i, binary_string in enumerate(sequence):
        if i > 0:
            if int(sequence[i-1], 2) % 2 != 0:
                plt.plot(i, int(binary_string, 2), 'ro')  # Red dot for 3n+1
            else:
                plt.plot(i, int(binary_string, 2), 'bo')  # Blue dot for n/2
        else:
            plt.plot(i, int(binary_string, 2), 'go')  # Green dot for the start
        plt.text(i, int(binary_string, 2), binary_string, ha='center', va='bottom')

    plt.plot(y_values, [int(s, 2) for s in sequence], 'k-', linewidth=0.5)

    plt.xlabel("Step")
    plt.ylabel("Value (Decimal, Log Scale)")
    plt.title(f"Collatz Sequence in Binary for {start_number} (Log Scale)")
    plt.yscale('log')  # Set logarithmic scale for y-axis
    plt.grid(True)
    plt.show()
    
def plot_binary_sequence_individual(sequence, start_number):
    """
    Plots the binary sequence individually
    """
    y_values = list(range(len(sequence)))

    plt.figure(figsize=(10, 5))

    for i, binary_string in enumerate(sequence):
        if i > 0:
            # Check if the previous step was 3n+1
            if int(sequence[i-1], 2) % 2 != 0:
                plt.plot(i, int(binary_string, 2), 'ro')  # Red dot for 3n+1
            else:
                plt.plot(i, int(binary_string, 2), 'bo')  # Blue dot for n/2
        else:
            plt.plot(i, int(binary_string, 2), 'go')  # Green dot for the start

        plt.text(i, int(binary_string, 2), binary_string, ha='center', va='bottom')
    
    plt.plot(y_values, [int(s, 2) for s in sequence], 'k-', linewidth=0.5)

    plt.xlabel("Step")
    plt.ylabel("Value (Decimal)")
    plt.title(f"Collatz Sequence in Binary for {start_number}")
    plt.grid(True)
    plt.show()

def plot_multiple_binary_sequences(start_numbers):
    """
    Plots multiple binary sequences in individual subplots.
    """
    num_plots = len(start_numbers)
    fig, axes = plt.subplots(num_plots, 1, figsize=(10, 5 * num_plots), sharex=True)

    for i, start_number in enumerate(start_numbers):
        sequence = binary_collatz_sequence(start_number)
        y_values = list(range(len(sequence)))

        ax = axes[i]

        for j, binary_string in enumerate(sequence):
            if j > 0:
                if int(sequence[j-1], 2) % 2 != 0:
                    ax.plot(j, int(binary_string, 2), 'ro')
                else:
                    ax.plot(j, int(binary_string, 2), 'bo')
            else:
                ax.plot(j, int(binary_string, 2), 'go')

            ax.text(j, int(binary_string, 2), binary_string, ha='center', va='bottom')

        ax.plot(y_values, [int(s, 2) for s in sequence], 'k-', linewidth=0.5)

        ax.set_ylabel(f"{start_number}\nValue (Decimal)")
        ax.set_title(f"Collatz Sequence in Binary for {start_number}")
        ax.grid(True)

    plt.xlabel("Step")
    plt.tight_layout()
    plt.show()

def binary_collatz_sequence(n):
    sequence = [bin(n)[2:]]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(bin(n)[2:])
    return sequence

def find_convergence_points(start_range, end_range, power_limit):
    """
    Identifies convergence points (powers of two) in Collatz sequences.
    """
    convergences = {}
    for start_number in range(start_range, end_range + 1):
        sequence = binary_collatz_sequence(start_number)
        for binary_string in sequence:
            decimal_value = int(binary_string, 2)
            if decimal_value not in convergences:
                convergences[decimal_value] = []
            convergences[decimal_value].append(start_number)

    # Filter for powers of two up to the specified limit
    powers_of_two = {2**i for i in range(power_limit)}
    filtered_convergences = {
        value: predecessors
        for value, predecessors in convergences.items()
        if value in powers_of_two
    }

    return filtered_convergences

test_numbers = [6, 15, 27, 53, 106, 89, 115, 213]  # Add more numbers
for num in test_numbers:
    sequence = collatz_sequence(num)
    print(f"Sequence for {num} (Binary: {bin(num)[2:]}): {sequence}")
    if contains_101_pattern(num):
        print(f"{num} contains the '101' pattern.")
        if any(is_in_S1(int(s, 2)) for s in sequence):
            print(f"{num} reaches S1.")
        else:
            print(f"{num} does not reach S1 (within the observed sequence).")
    else:
        print(f"{num} does not contain the '101' pattern.")
    print("-" * 20)

# Example usage:
start_range = 1
end_range = 100000
power_limit = 32  # Check up to 2^6 = 64

convergence_points = find_convergence_points(start_range, end_range, power_limit)

# Print convergence points that have more than one predecessor
for value, predecessors in convergence_points.items():
    print("-" * 20)
    print(f"Convergence point: {value} (Binary: {bin(value)[2:]})")
    print(f"Predecessors: {len(predecessors)}")
    print("-" * 20)

'''
def find_convergence_points(start_range, end_range):
    """
    Identifies convergence points in Collatz sequences within a given range.
    """
    convergences = {}  # Dictionary to store convergence points and their predecessors
    for start_number in range(start_range, end_range + 1):
        sequence = binary_collatz_sequence(start_number)
        for binary_string in sequence:
            decimal_value = int(binary_string, 2)
            if decimal_value not in convergences:
                convergences[decimal_value] = []
            convergences[decimal_value].append(start_number)
    return convergences

# Example usage:
start_range = 1
end_range = 100
convergence_points = find_convergence_points(start_range, end_range)

# Print convergence points that have more than one predecessor
for value, predecessors in convergence_points.items():
    if len(predecessors) > 1:
        print(f"Convergence point: {value} (Binary: {bin(value)[2:]})")
        print(f"Predecessors: {predecessors}")
        print("-" * 20)
'''

# Example usage:
start_numbers = [7, 11, 341, 27]  # Example start numbers

# For multiple plots in a single figure (no log scale):
# plot_multiple_binary_sequences(start_numbers)