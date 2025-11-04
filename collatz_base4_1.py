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

# Test with some interesting starting numbers
test_numbers = [
    7,    # Mersenne number
    27,   # Known long sequence
    85,   # L-type harbor
    341,  # Another L-type harbor
    127,  # Larger Mersenne number
]

analyze_multiple_starts(test_numbers)