import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

def calculate_distances(binary_string):
    """Calculate normalized L, M, P distances for a binary number."""
    # Power of Two distance (P)
    first_one = binary_string.find('1')
    p_distance = binary_string.count('1', first_one + 1) + first_one
    
    # Mersenne distance (M)
    m_distance = binary_string.count('0')
    
    # L-type Harbor distance (L)
    l_distance = 0
    if first_one != -1:
        trimmed = binary_string[first_one:]
        expected = '1'
        for bit in trimmed:
            if bit != expected:
                l_distance += 1
            expected = '0' if expected == '1' else '1'
        if len(trimmed) % 2 == 0:
            l_distance += 1
        l_distance += first_one
    
    # Normalize distances
    total = p_distance + m_distance + l_distance
    if total == 0:
        return 0, 0, 0
    
    return (p_distance/total, m_distance/total, l_distance/total)

def collatz_sequence_length(n):
    """Calculate steps to reach a power of two."""
    steps = 0
    while n > 1 and not (n & (n - 1) == 0):  # While not a power of 2
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        steps += 1
    return steps

def generate_test_numbers(max_bits=12, samples_per_length=100):
    """Generate test numbers with varying consecutive ones."""
    numbers = []
    for consecutive_ones in range(1, max_bits + 1):
        count = 0
        attempts = 0
        while count < samples_per_length and attempts < 1000:
            n = random.randint(1, 2**(consecutive_ones + 5))
            binary = bin(n)[2:]
            if binary.count('1') == consecutive_ones:
                numbers.append(n)
                count += 1
            attempts += 1
    return numbers

def plot_ternary_space_with_sequence_length(numbers):
    """Create enhanced ternary plot with sequence length information."""
    fig = plt.figure(figsize=(15, 10))
    
    # Create main ternary plot
    ax = fig.add_subplot(121)
    
    # Calculate and plot points
    points_data = []
    for n in numbers:
        binary = bin(n)[2:]
        p, m, l = calculate_distances(binary)
        seq_len = collatz_sequence_length(n)
        points_data.append((p, m, l, seq_len))
    
    # Convert to numpy array for easier manipulation
    points_array = np.array(points_data)
    
    # Normalize sequence lengths for color mapping
    normalized_lengths = points_array[:,3] / max(points_array[:,3])
    
    # Plot points
    scatter = ax.scatter(points_array[:,1], points_array[:,2],
                        c=normalized_lengths, cmap='viridis',
                        s=50, alpha=0.6)
    
    # Add colorbar
    plt.colorbar(scatter, label='Normalized Sequence Length')
    
    # Add vertex labels
    plt.annotate('P', xy=(0, 0))
    plt.annotate('M', xy=(1, 0))
    plt.annotate('L', xy=(0.5, np.sqrt(3)/2))
    
    # Set labels and title
    plt.xlabel('M-distance (normalized)')
    plt.ylabel('L-distance (normalized)')
    plt.title('Ternary Space with Sequence Length')
    
    # Add sequence length vs consecutive ones plot
    ax2 = fig.add_subplot(122)
    consecutive_ones = [bin(n)[2:].count('1') for n in numbers]
    sequence_lengths = [collatz_sequence_length(n) for n in numbers]
    
    ax2.scatter(consecutive_ones, sequence_lengths, alpha=0.6)
    ax2.set_xlabel('Number of Consecutive Ones')
    ax2.set_ylabel('Sequence Length')
    ax2.set_title('Sequence Length vs Consecutive Ones')
    
    plt.tight_layout()
    plt.show()

# Generate and plot test data
test_numbers = generate_test_numbers(12, 100)
plot_ternary_space_with_sequence_length(test_numbers)