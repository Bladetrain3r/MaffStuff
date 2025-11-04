
import random
import time
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt
import numpy as np

def is_power_of_two(n):
    """Checks if a number is a power of two."""
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1

def collatz_sequence_to_power_of_two(n, memo={}):
    """
    Generates the Collatz sequence for a given number n until a power of two is reached, using memoization.
    Returns the sequence and the number of steps to reach the power of two.
    """
    if n in memo:
        return memo[n], len(memo[n]) - 1 # Return memoized result if available

    sequence = [n]
    steps = 0
    while not is_power_of_two(n):
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
        steps += 1

        if n in memo: # Check if remaining sequence is already memoized
          memo[sequence[0]] = sequence + memo[n][1:]
          return memo[sequence[0]], len(memo[sequence[0]]) - 1

    memo[sequence[0]] = sequence  # Memoize the result
    return sequence, steps

def collatz_sequence_to_power_of_two_old(n):
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

def count_consecutive_ones(n):
    """Counts the maximum number of consecutive 1s in the binary representation of n."""
    binary_string = bin(n)[2:]
    max_consecutive = 0
    current_consecutive = 0
    for bit in binary_string:
        if bit == '1':
            current_consecutive += 1
            max_consecutive = max(max_consecutive, current_consecutive)
        else:
            current_consecutive = 0
    return max_consecutive

def analyze_consecutive_ones_vs_steps(max_consecutive_ones, num_samples_per_length):
    """
    Analyzes the relationship between the number of consecutive 1s and the number of 3n+1 steps to reach a power of two.
    """
    start_time = time.time()
    results = []
    for length in range(1, max_consecutive_ones + 1):
        for _ in range(num_samples_per_length):
            # Generate a random number with the specified number of consecutive 1s
            num = random.randint(0, 2**(length + 5))
            while count_consecutive_ones(num) != length:
                num = random.randint(0, 2**(length + 5))

            sequence, steps = collatz_sequence_to_power_of_two(num)
            results.append({'consecutive_ones': length, 'steps': steps, 'number': num})

    # Separate the results into two lists for plotting
    consecutive_ones = [result['consecutive_ones'] for result in results]
    steps_to_power_of_two = [result['steps'] for result in results]

    end_time = time.time()

    print(f"Execution time for {max_consecutive_ones} bits and {num_samples_per_length} samples per bit added: {end_time - start_time:.2f} seconds")

    # Create the scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(consecutive_ones, steps_to_power_of_two, alpha=0.7)
    plt.xlabel("Maximum Consecutive 1s in Binary Representation")
    plt.ylabel("Number of Steps to Reach a Power of Two")
    plt.title("Consecutive 1s vs. Steps to Power of Two")
    plt.grid(True)
    plt.show()

def analyze_number(num):
    """Analyzes a single number and returns the results."""
    sequence, steps = collatz_sequence_to_power_of_two(num)
    consecutive_ones = count_consecutive_ones(num)
    return {
        'number': num,
        'consecutive_ones': consecutive_ones,
        'steps': steps
    }

def analyze_consecutive_ones_vs_steps_parallel(max_consecutive_ones, num_samples_per_length):
    """
    Analyzes the relationship between the number of consecutive 1s and the 
    number of 3n+1 steps to reach a power of two, using multiple processes.
    """
    results = []

    start_time = time.time()
    
    # Use a with statement to ensure proper closing of the pool
    with Pool(processes=cpu_count()) as pool:  # Use all available CPU cores
      for length in range(1, max_consecutive_ones + 1):
          numbers = set()
          while len(numbers) < num_samples_per_length:
              # Generate a random number with the specified number of consecutive 1s
              num = random.randint(0, 2**(length + 5))
              if count_consecutive_ones(num) == length:
                numbers.add(num)

          # Apply analyze_number to each number in parallel
          for result in pool.map(analyze_number, numbers):
              results.append(result)

    # Separate the results into two lists for plotting
    consecutive_ones = [result['consecutive_ones'] for result in results]
    steps_to_power_of_two = [result['steps'] for result in results]

    end_time = time.time()

    print(f"Execution time: {end_time - start_time:.2f} seconds")

    # Create the scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(consecutive_ones, steps_to_power_of_two, alpha=0.7)
    plt.xlabel("Maximum Consecutive 1s in Binary Representation")
    plt.ylabel("Number of Steps to Reach a Power of Two")
    plt.title("Consecutive 1s vs. Steps to Power of Two")
    plt.grid(True)
    plt.show()

# Start time

# Example usage:
analyze_consecutive_ones_vs_steps(10, 1000)  # Test numbers with up to 10 consecutive 1s, 100 samples each
analyze_consecutive_ones_vs_steps(11, 1000)  # Test numbers with up to 10 consecutive 1s, 100 samples each
analyze_consecutive_ones_vs_steps(12, 1000)  # Test numbers with up to 10 consecutive 1s, 100 samples each
analyze_consecutive_ones_vs_steps(10, 10)  # Test numbers with up to 10 consecutive 1s, 100 samples each
analyze_consecutive_ones_vs_steps(10, 100)  # Test numbers with up to 10 consecutive 1s, 100 samples each
analyze_consecutive_ones_vs_steps(10, 1000)  # Test numbers with up to 10 consecutive 1s, 100 samples each
