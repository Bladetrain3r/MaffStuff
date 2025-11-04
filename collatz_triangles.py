import matplotlib.pyplot as plt
import numpy as np

# ... (your existing functions for calculating P-distance, M-distance, L-distance)

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

# Example usage:
test_numbers = [2, 3, 5, 7, 15, 21, 27, 31, 42, 55, 63, 85, 101, 127, 341, 503]  # Add more numbers
plot_triangle_space(test_numbers)