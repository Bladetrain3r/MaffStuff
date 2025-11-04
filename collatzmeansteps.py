import matplotlib.pyplot as plt
import numpy as np

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

# Example usage:
start_range = 1
end_range = 100
results = []

for i in range(start_range, end_range + 1):
    if not is_power_of_two(i) and not is_primary_harbor(i):
      sequence, steps = collatz_sequence_to_power_of_two(i)
      results.append({'number': i, 'steps': steps})
      print(f"Number: {i}, Steps to reach a power of two: {steps}")

# Calculate statistics
steps_array = np.array([result['steps'] for result in results])
mean_steps = np.mean(steps_array)
median_steps = np.median(steps_array)
std_dev_steps = np.std(steps_array)

print(f"\nMean steps: {mean_steps:.2f}")
print(f"Median steps: {median_steps}")
print(f"Standard deviation of steps: {std_dev_steps:.2f}")

# Generate histogram
plt.figure(figsize=(10, 6))
plt.hist(steps_array, bins=range(min(steps_array), max(steps_array) + 1), edgecolor='black')
plt.xlabel("Number of Steps to Reach a Power of Two")
plt.ylabel("Frequency")
plt.title("Distribution of Steps to Reach a Power of Two")
plt.grid(True)
plt.show()