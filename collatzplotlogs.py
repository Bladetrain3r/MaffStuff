import matplotlib.pyplot as plt
import numpy as np

def collatz_sequence(n):
    """Generates the Collatz sequence for a given number n."""
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

def calculate_slopes(sequence):
    """
    Calculates the cumulative effect of the positive and negative slopes 
    in logarithmic space for a given Collatz sequence.
    """
    log_sequence = np.log2(sequence)
    positive_slope = 0
    negative_slope = 0
    positive_slopes = []
    negative_slopes = []

    for i in range(len(sequence) - 1):
        if sequence[i] % 2 != 0:  # Odd number, 3n+1 step
            positive_slope += log_sequence[i+1] - log_sequence[i]
        else:  # Even number, n/2 step
            negative_slope += -1  # Each division by 2 contributes -1
        
        positive_slopes.append(positive_slope)
        negative_slopes.append(negative_slope)
    
    return positive_slopes, negative_slopes

def plot_slope_battle(sequence, start_number, label=None):
    """
    Plots the cumulative positive and negative slopes for a Collatz sequence.
    """
    positive_slopes, negative_slopes = calculate_slopes(sequence)
    
    plt.figure(figsize=(10, 6))
    
    plt.plot(positive_slopes, label='Cumulative Positive Slope (3n+1)', color='red')
    plt.plot(negative_slopes, label='Cumulative Negative Slope (n/2)', color='blue')
    
    # Find the point where the negative slope surpasses the positive slope
    convergence_point = None
    for i in range(len(positive_slopes)):
        if negative_slopes[i] < positive_slopes[i]:
            convergence_point = i
            break

    if convergence_point is not None:
        plt.axvline(x=convergence_point, color='green', linestyle='--', label='Convergence Point')

    plt.xlabel("Step")
    plt.ylabel("Cumulative Slope (Logarithmic Space)")
    plt.title(f"Collatz Sequence Slope Battle for {start_number}{' (' + label + ')' if label else ''}")
    plt.legend()
    plt.grid(True)
    plt.show()
    

# Test numbers
numbers = {
    5: "Primary Harbor (L(2))",
    21: "Primary Harbor (L(3))",
    87381: "Primary Harbor (L(9))",
    3: "Secondary Harbor (S(3))",
    11: "Proto-Harbor",
    7: "Leads to Proto-Harbor 11",
    31: "Stubborn Prime",
    41: "Stubborn Prime",
    27: "Known Long Sequence",
    19: "Random",
    42: "interesting",
    134: "Leads to 40"
}

# Plot slope battles for each number
for number, label in numbers.items():
    sequence = collatz_sequence(number)
    plot_slope_battle(sequence, number, label)
