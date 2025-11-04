def is_near_miss_bl_minus_1(n):
    """
    Checks if a number is one less than a 'bit limit - 1' number.
    """
    # Check if n+1 is of the form 2^k - 1
    if (n + 1) & (n + 2) != 0:  # Efficiently checks if n+2 is a power of 2
        return False
      
    binary_string = bin(n)[2:]
    
    
    return all(bit == '1' for bit in binary_string[:-1]) and binary_string[-1] == '0'

# ... (other functions: collatz_sequence, etc.)

# Test near misses
test_numbers = [6, 14, 26, 28, 30, 62, 126]
for num in test_numbers:
    sequence = collatz_sequence(num)
    print(f"Sequence for {num} (Binary: {bin(num)[2:]}): {sequence}")
    if is_near_miss_bl_minus_1(num):
        print(f"{num} is one less than a BL-1 number.")
        print(f"It halves to: {num // 2}, which is a BL-1 number.")
    else:
        print(f"{num} is not one less than a BL-1 number.")
    print("-" * 20)