from random import randint as randy

def to_base4(x):
    if x == 0:
        return "0"
    digits = []
    while x > 0:
        digits.append(str(x % 4))
        x //= 4
    return "".join(reversed(digits))

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
    131071, # Big number
    524287, # Bigger number
    randy(1, 1000000), # Random number
]

analyze_multiple_starts(test_numbers)

def verify_length_bounds(max_n=10000):
    """Verify base-4 length change bounds for Collatz operations."""
    
    def base4_length(n):
        """Calculate length of number in base-4."""
        if n == 0:
            return 1
        length = 0
        while n:
            length += 1
            n //= 4
        return length
    
    # Track maximum observed changes
    max_increase = 0
    max_decrease = 0
    example_increase = None
    example_decrease = None
    
    for n in range(1, max_n + 1):
        current_len = base4_length(n)
        
        if n % 2 == 1:  # Odd number
            next_n = 3 * n + 1
            next_len = base4_length(next_n)
            change = next_len - current_len
            
            if change > max_increase:
                max_increase = change
                example_increase = (n, next_n)
                
        else:  # Even number
            next_n = n // 2
            next_len = base4_length(next_n)
            change = next_len - current_len
            
            if change < max_decrease:
                max_decrease = change
                example_decrease = (n, next_n)
    
    print("\nBase-4 Length Change Analysis:")
    print(f"Maximum length increase: {max_increase}")
    if example_increase:
        print(f"Example increase: {example_increase[0]} -> {example_increase[1]}")
        print(f"In base 4: {to_base4(example_increase[0])} -> {to_base4(example_increase[1])}")
    
    print(f"\nMaximum length decrease: {max_decrease}")
    if example_decrease:
        print(f"Example decrease: {example_decrease[0]} -> {example_decrease[1]}")
        print(f"In base 4: {to_base4(example_decrease[0])} -> {to_base4(example_decrease[1])}")
    
    return max_increase, max_decrease

# Run verification
verify_length_bounds()