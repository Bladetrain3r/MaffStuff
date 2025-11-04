import matplotlib.pyplot as plt
import numpy as np
from random import randint as randy

def generalized_collatz_step(n: int, k: int) -> int:
    """Apply one step of k-generalized Collatz transformation"""
    div_power = 2**(k-1)
    if n % div_power == 0:
        return n // div_power
    else:
        multiplier = 2**k - 1
        adder = 2**(k-1) - 1
        return multiplier * n + adder

def analyze_sequence(start: int, k: int, max_steps: int = 10000, max_value: int = 10**256) -> dict:
    """Analyze a sequence with given k value"""
    sequence = [start]
    current = start
    
    for step in range(max_steps):
        current = generalized_collatz_step(current, k)
        if current > max_value:
            return {
                'converged': False,
                'length': step + 1,
                'max_value': float(max(sequence)),  # Convert to float
                'sequence': sequence,
                'reason': 'exceeded_max'
            }
        
        sequence.append(current)
        
        if current == 1:
            return {
                'converged': True,
                'length': step + 1,
                'max_value': float(max(sequence)),  # Convert to float
                'sequence': sequence,
                'reason': 'reached_one'
            }
            
        if len(sequence) > 2 and sequence[-1] == sequence[-2]:
            return {
                'converged': False,
                'length': step + 1,
                'max_value': float(max(sequence)),  # Convert to float
                'sequence': sequence,
                'reason': 'cycle_detected'
            }
    
    return {
        'converged': False,
        'length': max_steps,
        'max_value': float(max(sequence)),  # Convert to float
        'sequence': sequence,
        'reason': 'max_steps'
    }

# Test range of k values
k_values = list(range(2, 12))  # Convert to list for easier plotting
therandy = randy(1, 1000)
test_numbers = [3, 7, 15, 31, 63, 127, 255, 341, 85, 503, randy(1, 1000), therandy*3, therandy*7, therandy*15, therandy*31, therandy*63, therandy*127, therandy*255, therandy*341, therandy*85, therandy*503]

# Create visualizations
fig = plt.figure(figsize=(15, 15))

# Plot 1: Sequence lengths
plt.subplot(3, 1, 1)
for k in k_values:
    lengths = [analyze_sequence(n, k)['length'] for n in test_numbers]
    plt.plot(test_numbers, lengths, 'o-', label=f'k={k}')

plt.xlabel('Starting Number')
plt.ylabel('Sequence Length')
plt.title('Sequence Lengths by k Value')
plt.grid(True)
plt.legend()
plt.yscale('log')

# Plot 2: Growth ratios
plt.subplot(3, 1, 2)
ratios = [(2**k - 1)/(2**(k-1)) for k in k_values]
plt.plot(k_values, ratios, 'ro-')
plt.axhline(y=2, color='g', linestyle='--', label='Limit (2.0)')
plt.xlabel('k Value')
plt.ylabel('Growth Ratio')
plt.title('Growth Ratio vs k')
plt.grid(True)
plt.legend()

# Plot 3: Maximum values reached
plt.subplot(3, 1, 3)
for k in k_values:
    max_values = [np.log2(float(analyze_sequence(n, k)['max_value'])) for n in test_numbers]
    plt.plot(test_numbers, max_values, 'o-', label=f'k={k}')

plt.xlabel('Starting Number')
plt.ylabel('Log₂(Maximum Value)')
plt.title('Maximum Values Reached (Log Scale)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()

# Print analysis
print("\nGrowth Ratio Analysis:")
print("-" * 60)
for k in k_values:
    ratio = (2**k - 1)/(2**(k-1))
    print(f"\nk={k}:")
    print(f"Multiplier: {2**k - 1}")
    print(f"Divisor: {2**(k-1)}")
    print(f"Ratio: {ratio:.4f}")
    print(f"Distance to limit: {(2 - ratio):.4f}")

# Analyze convergence for each k
print("\nConvergence Analysis:")
print("-" * 60)
for k in k_values:
    converged = 0
    total_steps = 0
    max_steps = 0
    
    print(f"\nk={k}:")
    for n in test_numbers:
        result = analyze_sequence(n, k)
        print(f"{n}: {result['reason']} in {result['length']} steps (max value: {result['max_value']:.2e})")
        if result['converged']:
            converged += 1
            total_steps += result['length']
            max_steps = max(max_steps, result['length'])
    
    if converged > 0:
        avg_steps = total_steps / converged
        print(f"Converged: {converged}/{len(test_numbers)}")
        print(f"Average steps when converging: {avg_steps:.1f}")
        print(f"Max steps when converging: {max_steps}")
    else:
        print("No convergent sequences found")