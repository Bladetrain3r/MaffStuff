import numpy as np
from collections import Counter

def convert_to_base(n, base):
    """Convert number to specified base representation."""
    if n == 0:
        return "0"
    
    digits = "0123456789ABCDEF"
    result = ""
    
    while n:
        result = digits[n % base] + result
        n //= base
    
    return result

def calculate_pattern_entropy(representation, pattern_length=2):
    """Calculate entropy of digit patterns in any base representation."""
    if len(representation) < pattern_length:
        return 0
    
    # Count frequency of patterns
    patterns = [representation[i:i+pattern_length] 
               for i in range(len(representation)-pattern_length+1)]
    counts = {}
    for pattern in patterns:
        counts[pattern] = counts.get(pattern, 0) + 1
    
    # Calculate entropy
    total = len(patterns)
    entropy = 0
    for count in counts.values():
        p = count / total
        entropy -= p * np.log2(p)
    
    return entropy

def analyze_base_entropy(n, bases=[2, 3, 4, 8, 10, 16]):
    """Analyze entropy of a number in different bases."""
    results = []
    
    for base in bases:
        representation = convert_to_base(n, base)
        entropy = calculate_pattern_entropy(representation)
        max_possible = np.log2(min(base**2, len(representation)))  # Maximum possible entropy for this base
        
        results.append({
            'base': base,
            'representation': representation,
            'entropy': entropy,
            'max_possible': max_possible,
            'normalized_entropy': entropy / max_possible if max_possible > 0 else 0
        })
    
    print("\nEntropy Analysis Across Bases for", n)
    print("\nBase\tRepresentation\tEntropy\tMax Possible\tNormalized")
    for r in results:
        print(f"{r['base']}\t{r['representation']}\t{r['entropy']:.3f}\t{r['max_possible']:.3f}\t{r['normalized_entropy']:.3f}")
    
    return results

def analyze_maximal_numbers_in_bases(bases=[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]):
    """Analyze known maximal sequence numbers across different bases."""
    # Known maximal numbers from our previous analysis
    maximal_numbers = [
        (3, 9, 16),      # k=3
        (4, 27, 108),    # k=4
        (5, 54, 109),    # k=5
        (6, 97, 115),    # k=6
        (7, 231, 124),   # k=7
        (8, 327, 140),   # k=8
        (9, 871, 175),   # k=9
        (10, 1161, 178), # k=10
        (11, 3711, 234), # k=11
        (12, 6171, 258), # k=12
        (13, 13255, 272),# k=13
        (14, 26623, 304) # k=14
    ]
    
    results = []
    
    for k, number, seq_length in maximal_numbers:
        base_representations = {}
        base_entropies = {}
        
        for base in bases:
            # Get representation in this base
            representation = convert_to_base(number, base)
            entropy = calculate_pattern_entropy(representation)
            max_possible = np.log2(min(base**2, len(representation)))
            normalized_entropy = entropy / max_possible if max_possible > 0 else 0
            
            base_representations[base] = representation
            base_entropies[base] = normalized_entropy
            
        results.append({
            'k': k,
            'number': number,
            'sequence_length': seq_length,
            'representations': base_representations,
            'entropies': base_entropies
        })
    
    # Print analysis
    print("\nAnalysis of Maximal Numbers Across Bases:")
    print("\nk\tNumber\tSeq_Len", end='')
    for base in bases:
        print(f"\tBase_{base}_Entropy", end='')
    print()
    
    for r in results:
        print(f"{r['k']}\t{r['number']}\t{r['sequence_length']}", end='')
        for base in bases:
            print(f"\t{r['entropies'][base]:.3f}", end='')
        print()
    
    # Analyze correlation between entropies and sequence length
    correlations = {}
    for base in bases:
        entropy_values = [r['entropies'][base] for r in results]
        sequence_lengths = [r['sequence_length'] for r in results]
        correlation = np.corrcoef(entropy_values, sequence_lengths)[0,1]
        correlations[base] = correlation
    
    print("\nCorrelation between entropy and sequence length by base:")
    for base, correlation in sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True):
        print(f"Base {base}: {correlation:.3f}")
    
    return results, correlations

def analyze_patterns_in_best_bases(results, correlations, top_n=3):
    """Analyze patterns in the bases showing strongest correlation with sequence length."""
    # Get top correlated bases
    top_bases = sorted(correlations.items(), key=lambda x: abs(x[1]), reverse=True)[:top_n]
    
    print(f"\nDetailed Pattern Analysis for Top {top_n} Bases:")
    
    for base, correlation in top_bases:
        print(f"\nBase {base} (correlation: {correlation:.3f}):")
        print("Number\tRepresentation\tDigit Distribution")
        
        for r in results:
            representation = r['representations'][base]
            # Count digit frequencies
            digit_counts = Counter(representation)
            digit_dist = ' '.join(f"{d}:{digit_counts[d]}" for d in sorted(digit_counts.keys()))
            
            print(f"{r['number']}\t{representation}\t{digit_dist}")

# Analyze 327 across different bases
entropy_results = analyze_base_entropy(327)

# Also analyze a few other significant numbers for comparison
print("\nComparison with other significant numbers:")
for n in [255, 511, 85, 341]:  # Mersenne and L-type examples
    analyze_base_entropy(n)

results, correlations = analyze_maximal_numbers_in_bases()

analyze_patterns_in_best_bases(results, correlations)