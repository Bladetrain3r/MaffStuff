class MaximalSequenceAnalyzer:
    def __init__(self):
        # Known maximal sequence numbers and their lengths
        self.maximal_numbers = [
            (3, 9, 16),      # k, number, sequence length
            (4, 27, 108),
            (5, 54, 109),
            (6, 97, 115),
            (7, 231, 124),
            (8, 327, 140),
            (9, 871, 175),
            (10, 1161, 178),
            (11, 3711, 234),
            (12, 6171, 258),
            (13, 13255, 272),
            (14, 26623, 304)
        ]
    
    def to_base4(self, n):
        """Convert number to base-4 representation."""
        if n == 0:
            return "0"
        digits = []
        while n:
            digits.append(str(n % 4))
            n //= 4
        return "".join(reversed(digits))
    
    def get_pattern_sequence(self, n):
        """Get sequence of base-4 patterns in a number."""
        base4 = self.to_base4(n)
        return [base4[i:i+2] for i in range(len(base4)-1)]
    
    def analyze_maximal_patterns(self):
        """Analyze pattern combinations in maximal sequences."""
        results = []
        
        for k, number, length in self.maximal_numbers:
            base4 = self.to_base4(number)
            patterns = self.get_pattern_sequence(number)
            
            result = {
                'k': k,
                'number': number,
                'sequence_length': length,
                'base4': base4,
                'patterns': patterns,
                'pattern_counts': {},
                'pattern_sequence': patterns
            }
            
            # Count pattern occurrences
            for pattern in patterns:
                result['pattern_counts'][pattern] = result['pattern_counts'].get(pattern, 0) + 1
            
            results.append(result)
        
        # Print analysis
        print("\nPattern Combination Analysis in Maximal Sequences:")
        print("\nk\tNumber\tLength\tBase-4\t\tPattern Distribution")
        
        for r in results:
            patterns = ' '.join(f"{p}:{c}" for p, c in sorted(r['pattern_counts'].items()))
            print(f"{r['k']}\t{r['number']}\t{r['sequence_length']}\t{r['base4']}\t{patterns}")
        
        # Analyze pattern transitions
        print("\nPattern Transition Analysis:")
        transitions = {}
        for r in results:
            for i in range(len(r['pattern_sequence']) - 1):
                current = r['pattern_sequence'][i]
                next_pattern = r['pattern_sequence'][i + 1]
                key = (current, next_pattern)
                transitions[key] = transitions.get(key, 0) + 1
        
        print("\nCommon Pattern Transitions:")
        for (p1, p2), count in sorted(transitions.items(), key=lambda x: x[1], reverse=True):
            print(f"{p1}->{p2}: {count} occurrences")
        
        return results

# Run analysis
analyzer = MaximalSequenceAnalyzer()
maximal_patterns = analyzer.analyze_maximal_patterns()