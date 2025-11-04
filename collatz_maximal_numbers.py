import numpy as np

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

# Run the analysis
results, correlations = analyze_maximal_numbers_in_bases()