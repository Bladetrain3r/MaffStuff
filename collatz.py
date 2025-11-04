import matplotlib.pyplot as plt
from random import randint

def is_power_of_two(n):
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1

def is_in_S1(n):
    while n % 2 == 0:
        n //= 2
    return n == 5

def is_in_S2(n):
    while n % 2 == 0:
        n //= 2
    return n == 3

def collatz_sequence(n, H):
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence


# Define the sets P, F, S1, and S2
P = {2**a for a in range(1, 11)}  # Powers of 2 (excluding 1)
F = {5}
S1 = {2**a * 5 for a in range(10)}  # Up to 5120
S2 = {2**a * 3 for a in range(10)}  # Up to 3072

# Define the set of harbors H
H = P.union(F, S1, S2)

"""
# Examine duplicate digits
duplicate_digit_numbers = [i * 10 + i for i in range(1, 100)]  # 11, 22, ..., 99

for n in duplicate_digit_numbers:
    sequence = collatz_sequence(n, H)
    print(f"Sequence for {n}: {sequence}")
    if any(x in H for x in sequence):
        print(f"{n} is a trapdoor")
        if n in H:
            print(f"{n} is also a harbor")
    else:
        print(f"{n} is an outlier")


# Test a specific prime number
n = 89
sequence = collatz_sequence(n, H)
print(f"Sequence for {n}: {sequence}")
if sequence[-1] == 1:
    print(f"Sequence reached 1")
    is_trapdoor = False
    for x in sequence:
        print(f"Checking if {x} is in H")
        if x in H:
            print(f"{x} is in H")
            is_trapdoor = True
            break

    if sequence[0] in H:
        print(f"{n} is a harbor")
    elif is_trapdoor:
        print(f"{n} is a trapdoor")
    else:
        print(f"{n} is an outlier")
else:
    print(f"Sequence for {n} did not reach 1")
"""

# Generate numbers 1-1000
numbers = list(range(1, 1001))
test_outliers = [randint(1, 10000) for _ in range(10)]

# Classify each number
harbors = []
trapdoors = []
outliers = []

suspected_outliers = test_outliers  # Add more as needed
for n in suspected_outliers:
    sequence = collatz_sequence(n, H)
    print(f"Sequence for {n}: {sequence}")
    if sequence[-1] == 1:  # Ensure the sequence reached 1
        if sequence[0] in H:
            print(f"{n} is a harbor")
        elif any(x in H for x in sequence):
            print(f"{n} is a trapdoor")
        else:
            print(f"{n} is an outlier")
            outliers.append(n) # Add confirmed outlier to list
    else:
        print(f"Sequence for {n} did not reach 1")

for n in numbers:
    sequence = collatz_sequence(n, H)
    if sequence[-1] == 1:  # Ensure the sequence reached 1
        if sequence[0] in H:
            harbors.append(n)
        elif any(x in H for x in sequence):
            trapdoors.append(n)
        else:
            outliers.append(n)

# Calculate coverage
coverage = (len(harbors) + len(trapdoors)) / len(numbers) * 100

# Create the number line plot
plt.figure(figsize=(20, 5))
plt.scatter(harbors, [0] * len(harbors), color='green', label='Harbors', s=10)
plt.scatter(trapdoors, [0] * len(trapdoors), color='blue', label='Trapdoors', s=10)
plt.scatter(outliers, [0] * len(outliers), color='red', label='Outliers', s=10)
plt.yticks([])
plt.xlabel("Number")
plt.title(f"Collatz Conjecture Coverage (1-1000)\nCoverage: {coverage:.2f}%")
plt.legend()
plt.grid(True)
plt.show()

print(f"Coverage: {coverage:.2f}%")
print(f"Number of harbors: {len(harbors)}")
print(f"Number of trapdoors: {len(trapdoors)}")
print(f"Number of outliers: {len(outliers)}")