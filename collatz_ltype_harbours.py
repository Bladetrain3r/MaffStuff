import math

def transform(n, k):
    """Apply (2^k-1)n + (2^(k-1)-1) transformation"""
    return (2**k - 1) * n + (2**(k-1) - 1)

def is_power_of_two(n):
    """Check if n is a power of 2"""
    return n > 0 and (n & (n-1)) == 0

# Test values
# Number of digits for the maximum number
nodigits = 7
test_n = set(range(1, 10**nodigits))
k_values = [2, 3, 4]

print("Testing if (2^k-1)n + (2^(k-1)-1) yields powers of 2:\n")

for k in k_values:
    print(f"k = {k} → transformation is ({2**k-1})n + {2**(k-1)-1}")
    
    for n in test_n:
        result = transform(n, k)
        power_check = is_power_of_two(result)
        
        # Show arithmetic
        calculation = f"({2**k-1})×{n} + {2**(k-1)-1} = {(2**k-1)*n} + {2**(k-1)-1} = {result}"
        
        power_text = ""
        if power_check:
            power = int(math.log2(result))
            power_text = f" = 2^{power}, Power of 2: True"
            power_in_binary = bin(n)[2:]
            print(f"  n = {n}: {calculation}{power_text}, n_in_binary: {power_in_binary}")
        else:
            if n % 1000000 == 0:
                print(f"  n = {n}: {calculation}, Power of 2: False")
    
    print()