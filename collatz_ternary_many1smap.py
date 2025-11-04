import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

def calculate_distances(n):
    """Calculate normalized P, M, L distances for a number."""
    binary = bin(n)[2:]
    
    # P-distance: ones after leftmost one
    first_one = binary.find('1')
    p_distance = binary.count('1', first_one + 1) + first_one
    
    # M-distance: total zeros
    m_distance = binary.count('0')
    
    # L-distance: violations from alternating pattern
    l_distance = 0
    if first_one != -1:
        expected = '1'
        for bit in binary[first_one:]:
            if bit != expected:
                l_distance += 1
            expected = '1' if expected == '0' else '0'
    
    # Normalize
    total = float(p_distance + m_distance + l_distance)
    if total == 0:
        return 0, 0, 0
        
    return p_distance/total, m_distance/total, l_distance/total

def track_single_path(n, max_steps=1000):
    """Track a single number's Collatz path in ternary space."""
    path = []
    current = n
    seen = set()
    
    while not (current & (current - 1) == 0) and len(path) < max_steps:
        # Record current position
        p, m, l = calculate_distances(current)
        path.append([p, m, l])
        
        # Apply Collatz transformation
        if current % 2 == 0:
            current //= 2
        else:
            current = 3 * current + 1
            
        # Prevent cycles
        if current in seen:
            break
        seen.add(current)
    
    # Add final position
    p, m, l = calculate_distances(current)
    path.append([p, m, l])
    
    return np.array(path)

def generate_test_set():
    """Generate a diverse set of starting numbers with extended M and L type sequences."""
    test_cases = []
    
    # Powers of two (P-type baseline)
    test_cases.extend([16, 32, 64, 128, 256])
    
    # L-type harbors (increasing sequence)
    l_type = [(2**(2*k) - 1) // 3 for k in range(2, 7)]  # Generates 5, 21, 85, 341, 1365
    test_cases.extend(l_type)
    
    # Mersenne numbers (increasing sequence)
    mersenne = [(2**k - 1) for k in range(3, 8)]  # Generates 7, 15, 31, 63, 127
    test_cases.extend(mersenne)
    
    # Known interesting cases with longer sequences
    test_cases.extend([27, 41, 73, 351, 871, 1161])
    
    # Numbers with mixed characteristics
    test_cases.extend([11, 43, 79, 157, 313])
    
    # Add some higher-value L-type numbers
    test_cases.extend([5461, 21845])  # (2^14 - 1)/3 and (2^16 - 1)/3
    
    # Add some higher-value Mersenne numbers
    test_cases.extend([511, 1023])  # 2^9 - 1 and 2^10 - 1
    
    return test_cases

def visualize_paths(numbers, ax=None):
    """Create enhanced visualization of Collatz paths."""
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))
    
    # Plot each path with gradient coloring
    for n in numbers:
        path = track_single_path(n)
        
        # Create segments for line collection
        points = path[:, [1, 2]]  # Using M and L coordinates
        segments = np.concatenate([points[:-1, None], points[1:, None]], axis=1)
        
        # Create line collection with gradient colors
        lc = LineCollection(segments, cmap='viridis', alpha=0.6)
        lc.set_array(np.linspace(0, 1, len(path)-1))
        ax.add_collection(lc)
        
        # Mark start and end points
        ax.scatter(points[0, 0], points[0, 1], c='red', s=100, label='Start' if n == numbers[0] else "")
        ax.scatter(points[-1, 0], points[-1, 1], c='green', s=100, label='End' if n == numbers[0] else "")
        
    # Add labels and formatting
    ax.set_xlabel('M-distance (normalized)')
    ax.set_ylabel('L-distance (normalized)')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    return ax

def to_ternary_coords(p, m, l):
    """Convert normalized distances to ternary plot coordinates."""
    # Convert from barycentric to cartesian coordinates
    x = 0.5 * (2 * m + l)
    y = (np.sqrt(3)/2) * l
    return x, y

def plot_ternary_paths(numbers, max_paths=5):
    """Create ternary plot of Collatz paths."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Setup ternary plot
    ax1.plot([0, 1, 0.5, 0], [0, 0, np.sqrt(3)/2, 0], 'k-', alpha=0.5)
    
    # Plot paths
    colors = plt.cm.viridis(np.linspace(0, 1, len(numbers)))
    path_lengths = []
    
    for idx, n in enumerate(numbers[:max_paths]):
        path = track_single_path(n)
        path_lengths.append(len(path))
        
        # Convert to ternary coordinates
        x_coords = []
        y_coords = []
        for p, m, l in path:
            x, y = to_ternary_coords(p, m, l)
            x_coords.append(x)
            y_coords.append(y)
        
        # Plot path with gradient coloring
        points = np.column_stack([x_coords, y_coords])
        segments = np.column_stack([points[:-1], points[1:]])
        
        lc = LineCollection(segments.reshape(-1, 2, 2), cmap='viridis', alpha=0.6)
        lc.set_array(np.linspace(0, 1, len(path)-1))
        ax1.add_collection(lc)
        
        # Plot start and end points
        ax1.scatter(x_coords[0], y_coords[0], c='red', s=50)
        ax1.scatter(x_coords[-1], y_coords[-1], c='green', s=50)
    
    # Add vertex labels
    ax1.annotate('P', xy=(0, 0), xytext=(-0.05, -0.05))
    ax1.annotate('M', xy=(1, 0), xytext=(1.05, -0.05))
    ax1.annotate('L', xy=(0.5, np.sqrt(3)/2), xytext=(0.5, np.sqrt(3)/2 + 0.05))
    
    ax1.set_title('Collatz Paths in Ternary Space')
    ax1.axis('equal')
    
    # Plot path length distribution
    ax2.hist(path_lengths, bins='auto', edgecolor='black')
    ax2.set_xlabel('Path Length')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Path Lengths')
    
    plt.tight_layout()
    plt.show()

def create_full_visualization():
    """Create complete visualization with paths and annotations."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Plot paths
    test_numbers = generate_test_set()
    visualize_paths(test_numbers[:5], ax1)
    ax1.set_title('Collatz Paths in Ternary Space')
    
    # Plot vertex labels
    ax1.annotate('P', xy=(0, 0), xytext=(0.05, 0.05))
    ax1.annotate('M', xy=(1, 0), xytext=(0.95, 0.05))
    ax1.annotate('L', xy=(0.5, 0.866), xytext=(0.5, 0.9))
    
    # Add path distribution
    path_lengths = [len(track_single_path(n)) for n in test_numbers]
    ax2.hist(path_lengths, bins=20, edgecolor='black')
    ax2.set_xlabel('Path Length')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Distribution of Path Lengths')
    
    plt.tight_layout()
    plt.show()

def analyze_mersenne_transitions(start_k=3, end_k=32, focus_region=True):
    """
    Analyze transition patterns of Mersenne numbers near the PL edge.
    
    Args:
        start_k: Starting k for Mersenne numbers (2^k - 1)
        end_k: Ending k for Mersenne numbers
        focus_region: If True, zooms visualization to PL edge region
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
    
    # Track binary patterns and their positions
    pattern_transitions = []
    
    # Generate and track paths for each Mersenne number
    colors = plt.cm.viridis(np.linspace(0, 1, end_k - start_k))
    
    for idx, k in enumerate(range(start_k, end_k)):
        # Generate Mersenne number
        n = (2**k - 1)
        path = track_single_path(n)
        
        # Convert path to ternary coordinates
        points = []
        binary_patterns = []
        
        for p, m, l in path:
            x, y = to_ternary_coords(p, m, l)
            points.append((x, y))
            binary_patterns.append(bin(n)[2:])
        
        points = np.array(points)
        
        # Plot path with annotations
        if len(points) > 1:
            segments = np.column_stack([points[:-1], points[1:]])
            lc = LineCollection(segments.reshape(-1, 2, 2), 
                              color=colors[idx], alpha=0.6)
            ax1.add_collection(lc)
        
        # Mark start point and add k value label
        if len(points) > 0:
            ax1.scatter(points[0, 0], points[0, 1], c='red', s=50)
            ax1.annotate(f'k={k}', (points[0, 0], points[0, 1]), 
                        xytext=(5, 5), textcoords='offset points')
        
        # Store transition data
        pattern_transitions.append({
            'k': k,
            'patterns': binary_patterns,
            'positions': points
        })
    
    # Draw ternary triangle
    ax1.plot([0, 1, 0.5, 0], [0, 0, np.sqrt(3)/2, 0], 'k-', alpha=0.5)
    
    # Add vertex labels
    ax1.annotate('P', xy=(0, 0), xytext=(-0.05, -0.05))
    ax1.annotate('M', xy=(1, 0), xytext=(1.05, -0.05))
    ax1.annotate('L', xy=(0.5, np.sqrt(3)/2), xytext=(0.5, np.sqrt(3)/2 + 0.05))
    
    if focus_region:
        # Zoom to PL edge region
        ax1.set_xlim(-0.1, 0.4)
        ax1.set_ylim(-0.1, 0.4)
    
    ax1.set_title('Mersenne Number Transitions (PL Edge Focus)')
    
    # Plot transition analysis
    transition_lengths = [len(t['patterns']) for t in pattern_transitions]
    ax2.bar(range(start_k, end_k), transition_lengths)
    ax2.set_xlabel('k (Mersenne number 2^k - 1)')
    ax2.set_ylabel('Number of transitions')
    ax2.set_title('Transition Count vs Mersenne Number Size')
    
    plt.tight_layout()
    plt.show()
    
    return pattern_transitions

def analyze_binary_changes(pattern_transitions):
    """Analyze how binary patterns change during transitions."""
    for transition in pattern_transitions:
        k = transition['k']
        patterns = transition['patterns']
        
        if len(patterns) > 1:
            print(f"\nAnalyzing Mersenne number k={k} (2^{k} - 1):")
            for i in range(len(patterns)-1):
                current = patterns[i]
                next_pattern = patterns[i+1]
                print(f"Step {i}: {current} -> {next_pattern}")
                
                # Calculate positions where bits changed
                changes = []
                min_len = min(len(current), len(next_pattern))
                for pos in range(min_len):
                    if current[pos] != next_pattern[pos]:
                        changes.append(pos)
                
                print(f"Bit changes at positions: {changes}")

# Example usage
pattern_transitions = analyze_mersenne_transitions(3, 32)
analyze_binary_changes(pattern_transitions)

def analyze_mersenne_properties(start_k=3, end_k=10):
    results = []
    for k in range(start_k, end_k + 1):
        # Generate Mersenne number and its full binary length cohort
        mersenne = 2**k - 1
        max_number = 2**(k+1) - 1
        
        # Track sequence lengths for all numbers of this length
        lengths = []
        trajectories = []
        
        # Sample numbers of same binary length
        for n in range(2**k, max_number + 1):
            path = track_single_path(n)
            lengths.append(len(path))
            
            # Calculate bounding box of trajectory
            if len(path) > 0:
                m_coords = path[:, 1]  # M-distance
                l_coords = path[:, 2]  # L-distance
                trajectories.append({
                    'number': n,
                    'm_bounds': (min(m_coords), max(m_coords)),
                    'l_bounds': (min(l_coords), max(l_coords))
                })
        
        # Get Mersenne trajectory
        mersenne_path = track_single_path(mersenne)
        
        results.append({
            'k': k,
            'mersenne': mersenne,
            'mersenne_length': len(mersenne_path),
            'max_other_length': max(lengths),
            'mean_length': np.mean(lengths),
            'is_maximum': len(mersenne_path) >= max(lengths),
            'trajectory_bounds': trajectories
        })
    
    return results

results = analyze_mersenne_properties(3, 16)

for result in results:
    print(f"K: {result['k']}, Mersenne: {result['mersenne']}, Mersenne Length: {result['mersenne_length']}, Max Other Length: {result['max_other_length']}, Mean Length: {result['mean_length']}, Is Maximum: {result['is_maximum']}")

def main():
    # Generate our test cases
    test_numbers = generate_test_set()
    
    # First, let's create the ternary plot with a subset of numbers
    # This will show the paths of the first 5 numbers in detail
    plot_ternary_paths(test_numbers, max_paths=10)
    
    # Then create the full visualization with all test cases
    create_full_visualization()

    # If you want to examine specific categories, you can create targeted visualizations
    # For example, to look at just Mersenne numbers:
    mersenne_numbers = [(2**k - 1) for k in range(3, 32)]
    plot_ternary_paths(mersenne_numbers, max_paths=len(mersenne_numbers))
    
    # Or just L-type harbors:
    l_type_numbers = [(2**(2*k) - 1) // 3 for k in range(2, 31)]
    plot_ternary_paths(l_type_numbers, max_paths=len(l_type_numbers))

# Run the visualization
# if __name__ == "__main__":
#    main()