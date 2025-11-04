import numpy as np
from collections import Counter

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
    
def analyze_binary_patterns_for_maxima(start_k=3, end_k=16):
    """Analyze binary patterns of numbers achieving maximum sequence lengths."""
    results = []
    
    for k in range(start_k, end_k + 1):
        # Analyze all numbers of length k
        max_length = 0
        max_numbers = []
        
        for n in range(2**k, 2**(k+1)):
            path_length = len(track_single_path(n))
            
            if path_length > max_length:
                max_length = path_length
                max_numbers = [n]
            elif path_length == max_length:
                max_numbers.append(n)
        
        # Analyze binary patterns of maximum achievers
        for n in max_numbers:
            binary = bin(n)[2:]
            
            # Calculate pattern statistics
            consecutive_ones = max(len(s) for s in binary.split('0'))
            total_ones = binary.count('1')
            zero_runs = max(len(s) for s in binary.split('1'))
            
            # Look for alternating patterns
            alternating_violations = 0
            expected = '1'
            for bit in binary:
                if bit != expected:
                    alternating_violations += 1
                expected = '0' if expected == '1' else '1'
            
            results.append({
                'k': k,
                'number': n,
                'binary': binary,
                'sequence_length': max_length,
                'consecutive_ones': consecutive_ones,
                'total_ones': total_ones,
                'zero_runs': zero_runs,
                'alternating_violations': alternating_violations
            })
    
    # Print analysis
    print("\nAnalysis of Maximum Sequence Length Numbers:")
    print("\nk\tNumber\tLength\tBinary\tCons.1s\tTotal 1s\tMax 0s\tAlt.Viol")
    for r in results:
        print(f"{r['k']}\t{r['number']}\t{r['sequence_length']}\t{r['binary']}\t{r['consecutive_ones']}\t{r['total_ones']}\t{r['zero_runs']}\t{r['alternating_violations']}")
    
    return results


def calculate_binary_entropy(binary_string):
    """Calculate Shannon entropy of binary pattern."""
    # Count frequency of patterns of length 2
    patterns = [binary_string[i:i+2] for i in range(len(binary_string)-1)]
    counts = Counter(patterns)
    total = len(patterns)
    
    # Calculate entropy
    entropy = 0
    for count in counts.values():
        p = count / total
        entropy -= p * np.log2(p)
    return entropy

def analyze_entropy_dynamics(n):
    """Analyze how entropy changes through Collatz sequence."""
    sequence = []
    current = n
    entropies = []
    
    while not (current & (current - 1) == 0):  # While not a power of 2
        sequence.append(current)
        binary = bin(current)[2:]
        entropies.append(calculate_binary_entropy(binary))
        
        if current % 2 == 0:
            current //= 2
        else:
            current = 3 * current + 1
    
    return sequence, entropies

def analyze_maximum_achievers_entropy():
    """Analyze entropy patterns of maximum sequence length numbers."""
    results = []
    
    for k in range(2, 10):
        max_length = 0
        max_number = None
        max_entropy = None
        
        for n in range(2**k, 2**(k+1)):
            path = track_single_path(n)
            if len(path) > max_length:
                max_length = len(path)
                max_number = n
                
        if max_number:
            binary = bin(max_number)[2:]
            initial_entropy = calculate_binary_entropy(binary)
            sequence, entropy_sequence = analyze_entropy_dynamics(max_number)
            
            results.append({
                'k': k,
                'number': max_number,
                'initial_entropy': initial_entropy,
                'mean_entropy': np.mean(entropy_sequence),
                'max_entropy': max(entropy_sequence),
                'sequence_length': max_length
            })
    
    return results

def analyze_sequence_max_entropy(n, verbose=False):
    """Analyze if and when a sequence reaches maximum entropy."""
    sequence = []
    current = n
    reached_max = False
    steps_to_max = 0
    
    while not (current & (current - 1) == 0):  # While not a power of 2
        sequence.append(current)
        binary = bin(current)[2:]
        entropy = calculate_binary_entropy(binary)
        
        if abs(entropy - 2.0) < 0.0001:  # Account for floating point precision
            reached_max = True
            break
            
        steps_to_max += 1
        
        if current % 2 == 0:
            current //= 2
        else:
            current = 3 * current + 1
    
    return {
        'number': n,
        'reached_max': reached_max,
        'steps_to_max': steps_to_max if reached_max else None,
        'sequence_length': len(sequence)
    }

def find_maxima_entropy_patterns(start_k=2, end_k=16):
    """Find numbers that achieve maximum entropy and compare to maxima sequences."""
    results = []
    
    for k in range(start_k, end_k + 1):
        # Find the maximum sequence length for this k
        max_length = 0
        max_numbers = []
        
        for n in range(2**k, 2**(k+1)):
            path = track_single_path(n)
            if len(path) > max_length:
                max_length = len(path)
                max_numbers = [n]
            elif len(path) == max_length:
                max_numbers.append(n)
        
        # Analyze maxima numbers
        for max_num in max_numbers:
            analysis = analyze_sequence_max_entropy(max_num)
            results.append({
                'k': k,
                'number': max_num,
                'sequence_length': max_length,
                'reaches_max_entropy': analysis['reached_max'],
                'steps_to_max': analysis['steps_to_max']
            })
    
    print("\nAnalysis of Maximum Length Sequences and Entropy:")
    print("\nk\tNumber\tLength\tReaches Max\tSteps to Max")
    for r in results:
        print(f"{r['k']}\t{r['number']}\t{r['sequence_length']}\t{r['reaches_max_entropy']}\t{r['steps_to_max']}")
    
    return results

# Run analysis
maxima_patterns = analyze_binary_patterns_for_maxima(2, 10)

# Additional statistical analysis
print("\nPattern Statistics Summary:")
print("\nAverage properties by binary length:")
k_groups = {}
for r in maxima_patterns:
    if r['k'] not in k_groups:
        k_groups[r['k']] = []
    k_groups[r['k']].append(r)

for k, group in sorted(k_groups.items()):
    avg_cons_ones = sum(r['consecutive_ones'] for r in group) / len(group)
    avg_total_ones = sum(r['total_ones'] for r in group) / len(group)
    avg_zero_runs = sum(r['zero_runs'] for r in group) / len(group)
    
    print(f"\nk={k}:")
    print(f"Average consecutive ones: {avg_cons_ones:.2f}")
    print(f"Average total ones: {avg_total_ones:.2f}")
    print(f"Average max zero run: {avg_zero_runs:.2f}")

results = analyze_maximum_achievers_entropy()

# Print results
print("\nEntropy Analysis of Maximum Sequence Length Numbers:")
print("\nk\tNumber\tLength\tInitial\tMean\tMax")
for r in results:
    print(f"{r['k']}\t{r['number']}\t{r['sequence_length']}\t{r['initial_entropy']:.3f}\t{r['mean_entropy']:.3f}\t{r['max_entropy']:.3f}")

maxima_entropy_results = find_maxima_entropy_patterns()