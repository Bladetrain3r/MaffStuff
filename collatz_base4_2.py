from random import randint as randy

def analyze_3n1_sequence(n, max_steps=50):
    """Analyze sequence of 3n+1 operations until power of 2 or max steps."""
    
    def to_base4(x):
        if x == 0:
            return "0"
        digits = []
        while x > 0:
            digits.append(str(x % 4))
            x //= 4
        return "".join(reversed(digits))
    
    def next_odd(x):
        """Apply 3n+1 and divide by 2 until odd."""
        x = 3 * x + 1
        while x % 2 == 0:
            x //= 2
        return x, bin(x).count('0')  # Return number and count of zeros
    
    sequence = []
    current = n
    seen = set()
    
    while not (current & (current - 1) == 0) and len(sequence) < max_steps:  # Continue until power of 2
        if current in seen:
            break
            
        base4 = to_base4(current)
        binary = bin(current)[2:]
        
        sequence.append({
            'number': current,
            'base4': base4,
            'binary': binary,
            'base4_length': len(base4),
            'binary_length': len(binary)
        })
        
        seen.add(current)
        current, zeros = next_odd(current)
    
    # Add final state if it's a power of 2
    if current & (current - 1) == 0:
        sequence.append({
            'number': current,
            'base4': to_base4(current),
            'binary': bin(current)[2:],
            'base4_length': len(to_base4(current)),
            'binary_length': len(bin(current)[2:])
        })
    
    return sequence

def analyze_multiple_starts(start_numbers):
    """Analyze 3n+1 sequences for multiple starting numbers."""
    for n in start_numbers:
        sequence = analyze_3n1_sequence(n)
        
        print(f"\nAnalysis for starting number {n}:")
        print("Step\tNumber\tBase-4\tBinary\tBase-4 Length")
        for i, state in enumerate(sequence):
            print(f"{i}\t{state['number']}\t{state['base4']}\t{state['binary']}\t{state['base4_length']}")
        
        if sequence[-1]['number'] & (sequence[-1]['number'] - 1) == 0:
            print("Reached power of two!")
        else:
            print("Max steps reached or cycle detected")

def analyze_pattern_changes(sequence):
    """Analyze how patterns change through the sequence."""
    
    def get_digit_distribution(base4_str):
        """Get distribution of digits in base-4 representation."""
        return {str(i): base4_str.count(str(i)) for i in range(4)}
    
    changes = []
    for i in range(len(sequence)-1):
        current = sequence[i]
        next_state = sequence[i+1]
        
        # Analyze digit distributions
        current_dist = get_digit_distribution(current['base4'])
        next_dist = get_digit_distribution(next_state['base4'])
        
        # Analyze length changes
        length_change = next_state['base4_length'] - current['base4_length']
        
        changes.append({
            'step': i,
            'from_number': current['number'],
            'to_number': next_state['number'],
            'length_change': length_change,
            'from_dist': current_dist,
            'to_dist': next_dist
        })
    
    return changes

def print_pattern_analysis(n):
    """Print detailed analysis of pattern changes for a number."""
    sequence = analyze_3n1_sequence(n)
    changes = analyze_pattern_changes(sequence)
    
    print(f"\nDetailed Pattern Analysis for {n}:")
    print("\nStep\tFrom\tTo\tLength Δ\tFrom Distribution\tTo Distribution")
    
    for change in changes:
        print(f"{change['step']}\t{change['from_number']}\t{change['to_number']}\t"
              f"{change['length_change']}\t{change['from_dist']}\t{change['to_dist']}")

# Analyze a few specific numbers in detail
for n in [27, 85, 127, 4543, 8191, 131071]:
    print_pattern_analysis(n)