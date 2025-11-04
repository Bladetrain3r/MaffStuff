def find_prime_harbors_7n_plus_3(power_limit):
    """
    Finds potential "prime harbors" for the 7n+3 transformation.

    Args:
        power_limit: The maximum power of 4 to consider.

    Returns:
        A list of odd integers n that satisfy 7n + 3 = 4^k.
    """
    prime_harbors = []
    for k in range(1, power_limit + 1):
        # Solve 7n + 3 = 4^k for n
        n = (4**k - 3) // 7
        if (4**k -3) % 7 == 0:
            if n % 2 != 0:  # Check if n is odd
                prime_harbors.append(n)
    return prime_harbors

# Example usage:
power_limit = 100000
prime_harbors = find_prime_harbors_7n_plus_3(power_limit)
print(f"Potential prime harbors for 7n+3 (up to 4^{power_limit}): {prime_harbors}")

def modified_collatz_sequence(n, max_steps=1000):
    """
    Generates a Collatz-like sequence using n/4 and 7n+3 rules.

    Args:
        n: The starting number.
        max_steps: The maximum number of steps to generate.

    Returns:
        A list representing the sequence, and a boolean indicating if the sequence reached 1.
    """
    sequence = [n]
    for _ in range(max_steps):
        if n == 1:
            return sequence, True
        if n % 4 == 0:
            n //= 4
        else:
            n = 7 * n + 3
        sequence.append(n)
    return sequence, False

# Test the found prime harbors
for harbor in prime_harbors:
    sequence, reached_one = modified_collatz_sequence(harbor)
    print(f"Sequence for {harbor}: {sequence}")
    if reached_one:
        print(f"{harbor} reached 1 in {len(sequence)} steps.")
    else:
        print(f"{harbor} did not reach 1 within the maximum steps.")
    print("-" * 20)