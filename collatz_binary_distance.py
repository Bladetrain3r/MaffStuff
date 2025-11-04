import random
import numpy as np
import matplotlib.pyplot as plt
import mpltern

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

def generate_pattern_number(pattern_type, min_bits=4, max_bits=128):
    """
    Generates a number matching a specific binary pattern.
    
    Args:
        pattern_type: 'P' for Power of Two, 'M' for Mersenne, 'L' for L-type Harbor
        min_bits: Minimum number of bits in the generated number
        max_bits: Maximum number of bits in the generated number
    
    Returns:
        tuple: (decimal_number, binary_string)
    """
    bits = random.randint(min_bits, max_bits)
    
    if pattern_type == 'P':  # Powers of Two (10000...)
        number = 1 << (bits - 1)  # Same as 2**(bits-1)
        binary = '1' + '0' * (bits - 1)
        
    elif pattern_type == 'M':  # Mersenne Numbers (11111...)
        number = (1 << bits) - 1  # Same as 2**bits - 1
        binary = '1' * bits
        
    elif pattern_type == 'L':  # L-type Harbors (10101...01)
        # Calculate how many '10' pairs we need
        pairs = (bits - 1) // 2
        binary = ''.join(['10' for _ in range(pairs)]) + '1'
        number = int(binary, 2)
    
    else:
        raise ValueError(f"Unknown pattern type: {pattern_type}")
        
    return number, binary

def validate_pattern(binary_string, pattern_type):
    """
    Validates if a binary string matches the specified pattern.
    
    Args:
        binary_string: String of 1s and 0s
        pattern_type: 'P', 'M', or 'L'
    
    Returns:
        bool: True if the pattern matches, False otherwise
    """
    if pattern_type == 'P':
        return binary_string.startswith('1') and set(binary_string[1:]) == {'0'}
    elif pattern_type == 'M':
        return set(binary_string) == {'1'}
    elif pattern_type == 'L':
        if not binary_string.endswith('1'):
            return False
        # Check for alternating 10 pattern
        for i in range(0, len(binary_string)-1, 2):
            if binary_string[i:i+2] != '10':
                return False
        return True
    return False

def generate_test_set(num_each=5):
    """
    Generates a test set with equal numbers of each pattern type.
    
    Args:
        num_each: Number of examples to generate for each pattern
    
    Returns:
        list: List of tuples (number, binary_string, pattern_type)
    """
    test_set = []
    for pattern in ['P', 'M', 'L']:
        for _ in range(num_each):
            number, binary = generate_pattern_number(pattern)
            if (number, binary, pattern) not in test_set:
                test_set.append((number, binary, pattern))
    return test_set

def calculate_p_distance(binary_string):
    """Calculates the P-distance of a binary string."""
    first_one = binary_string.find('1')
    if first_one == -1:
        return 0
    
    return binary_string.count('1', first_one + 1) + first_one

def calculate_m_distance(binary_string):
    """Calculates the M-distance of a binary string."""
    return binary_string.count('0')

def calculate_l_distance(binary_string):
    """Calculates the L-distance of a binary string."""
    
    first_one = binary_string.find('1')
    if first_one == -1:
        return 0
    
    trimmed_string = binary_string[first_one:]    
    
    violations = 0
    expected = '1'
    for bit in trimmed_string:
        if bit != expected:
            violations += 1
        if expected == '1':
            expected = '0'
        else:
            expected = '1'
            
    # Check if the pattern ends with something other than 1
    if (len(trimmed_string) % 2 == 0):
        violations += 1
    
    return violations + first_one

def calculate_convergence_index(n, w1, w2, w3):
    """Calculates the Convergence Index for a number."""
    binary_string = bin(n)[2:]
    p_distance = calculate_p_distance(binary_string)
    m_distance = calculate_m_distance(binary_string)
    l_distance = calculate_l_distance(binary_string)
    return w1 * p_distance + w2 * m_distance + w3 * l_distance

def plot_triangle_space(numbers):
    """
    Plots the numbers in the triangle space based on their P, M, and L distances.
    """
    p_distances = []
    m_distances = []
    l_distances = []

    for n in numbers:
        binary_string = bin(n)[2:]
        p_distances.append(calculate_p_distance(binary_string))
        m_distances.append(calculate_m_distance(binary_string))
        l_distances.append(calculate_l_distance(binary_string))

    # Normalize distances for plotting (you might need to adjust the scaling)
    p_distances = np.array(p_distances) / max(p_distances)
    m_distances = np.array(m_distances) / max(m_distances)
    l_distances = np.array(l_distances) / max(l_distances)
    
    # Placeholder for triangle plot - needs further development to properly represent
    # the distances in a triangular coordinate system.
    plt.figure(figsize=(8, 8))
    plt.scatter(m_distances, l_distances, c=p_distances, cmap='viridis', s=100, alpha=0.8)

    # Add vertices for P, M, and L
    plt.scatter(0, 0, marker='^', s=200, color='red', label='P (Power of Two)')  # Assuming M and L are 0 at P
    plt.scatter(1, 0, marker='^', s=200, color='green', label='M (Mersenne)')  # Assuming P and L are 0 at M
    plt.scatter(0, 1, marker='^', s=200, color='blue', label='L (Harbor)')  # Assuming P and M are 0 at L
    
    plt.xlabel("M-distance (Normalized)")
    plt.ylabel("L-distance (Normalized)")
    plt.title("Collatz Numbers in Triangle Space")
    plt.colorbar(label='P-distance (Normalized)')
    plt.legend()
    plt.grid(True)
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    plt.show()

def plot_ternary_space(numbers):
    """
    Plots the numbers in a ternary plot based on their P, M, and L distances.
    """
    p_distances = []
    m_distances = []
    l_distances = []

    for n in numbers:
        binary_string = bin(n)[2:]
        p_distances.append(calculate_p_distance(binary_string))
        m_distances.append(calculate_m_distance(binary_string))
        l_distances.append(calculate_l_distance(binary_string))

    # Normalize distances for ternary plot (sum of distances should be 1)
    total_distances = np.array(p_distances) + np.array(m_distances) + np.array(l_distances)
    p_distances = np.array(p_distances) / total_distances
    m_distances = np.array(m_distances) / total_distances
    l_distances = np.array(l_distances) / total_distances
    
    # Create ternary plot
    fig, ax = plt.subplots(figsize=(16, 16))
    ax = fig.add_subplot(111, projection='ternary')
    
    # Scatter plot of points
    ax.scatter(p_distances, m_distances, l_distances, c=p_distances, cmap='viridis', s=100, alpha=0.8)

    # Set labels and title
    ax.set_tlabel('P-distance')
    ax.set_llabel('M-distance')
    ax.set_rlabel('L-distance')
    ax.set_title("Collatz Numbers in Ternary Space")

    # Add vertices for P, M, and L
    ax.plot([1, 0, 0, 1], [0, 1, 0, 0], [0, 0, 1, 0], 'k-', lw=2) # Triangle outline

    # Display the plot
    plt.show()

def analyze_distance_vs_length(num_samples, max_val):
    """
    Analyzes the relationship between P, M, L distances and Collatz sequence length.
    """
    numbers = [random.randint(1, max_val) for _ in range(num_samples)]
    p_distances = []
    m_distances = []
    l_distances = []
    sequence_lengths = []

    for n in numbers:
        binary_string = bin(n)[2:]
        p_distances.append(calculate_p_distance(binary_string))
        m_distances.append(calculate_m_distance(binary_string))
        l_distances.append(calculate_l_distance(binary_string))
        sequence_lengths.append(len(collatz_sequence(n)))

    # Calculate correlations
    print(f"Correlation (P-distance, Sequence Length): {np.corrcoef(p_distances, sequence_lengths)[0, 1]:.4f}")
    print(f"Correlation (M-distance, Sequence Length): {np.corrcoef(m_distances, sequence_lengths)[0, 1]:.4f}")
    print(f"Correlation (L-distance, Sequence Length): {np.corrcoef(l_distances, sequence_lengths)[0, 1]:.4f}")

    # Scatter plots
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.scatter(p_distances, sequence_lengths, alpha=0.5)
    plt.xlabel("P-distance")
    plt.ylabel("Sequence Length")
    plt.title("P-distance vs. Sequence Length")

    plt.subplot(1, 3, 2)
    plt.scatter(m_distances, sequence_lengths, alpha=0.5)
    plt.xlabel("M-distance")
    plt.ylabel("Sequence Length")
    plt.title("M-distance vs. Sequence Length")

    plt.subplot(1, 3, 3)
    plt.scatter(l_distances, sequence_lengths, alpha=0.5)
    plt.xlabel("L-distance")
    plt.ylabel("Sequence Length")
    plt.title("L-distance vs. Sequence Length")

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Generate and test some examples
    test_set = generate_test_set(100)
    
    for number, binary, pattern in test_set:
        p_distance = calculate_p_distance(binary)
        m_distance = calculate_m_distance(binary)
        l_distance = calculate_l_distance(binary)
        ci = calculate_convergence_index(number, 1, -0.5, 2)
        
        print(f"Pattern {pattern}:")
        print(f"  Number: {number} (Binary: {binary})")
        print(f"  P-distance: {p_distance}")
        print(f"  M-distance: {m_distance}")
        print(f"  L-distance: {l_distance}")
        print(f"  Convergence Index: {ci}")
        print(f"  Valid pattern: {validate_pattern(binary, pattern)}")
        print("-" * 40)

    test_numbers = [number for number, _, _ in test_set]
    test_numbers.extend([number for number in range(1, 10000)])
    plot_triangle_space(test_numbers)
    plot_ternary_space(test_numbers)

    analyze_distance_vs_length(1000, 10000)