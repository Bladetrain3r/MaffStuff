class CollatzPatternAnalyzer:
    @staticmethod
    def to_base4(n):
        """Convert number to base-4 representation."""
        if n == 0:
            return "0"
        base4 = ""
        while n:
            base4 = str(n % 4) + base4
            n //= 4
        return base4
    
    @staticmethod
    def get_patterns(base4_str):
        """Extract two-digit patterns from base-4 string."""
        return [base4_str[i:i+2] for i in range(len(base4_str)-1)]
    
    @staticmethod
    def sequence_length(n, transform_func=None):
        """Calculate sequence length to first power of 2."""
        if transform_func is None:
            transform_func = lambda x: x // 2 if x % 2 == 0 else 3 * x + 1
            
        steps = 0
        current = n
        seen = set()
        
        while current > 1 and not (current & (current - 1) == 0):
            if current in seen:
                return steps, False  # Non-convergent
            seen.add(current)
            current = transform_func(current)
            steps += 1
            
        return steps, True  # Convergent

    def analyze_range(self, start_k=3, end_k=8):
        """Analyze pattern weights for a range of numbers."""
        pattern_data = {}
        max_length = 0
        
        # Collect pattern data
        for k in range(start_k, end_k + 1):
            for n in range(2**k, 2**(k+1)):
                seq_length, converged = self.sequence_length(n)
                if not converged:
                    continue
                    
                patterns = self.get_patterns(self.to_base4(n))
                max_length = max(max_length, seq_length)
                
                # Update pattern statistics
                for pattern in patterns:
                    if pattern not in pattern_data:
                        pattern_data[pattern] = {'occurrences': 0, 'total_length': 0, 'max_length': 0}
                    data = pattern_data[pattern]
                    data['occurrences'] += 1
                    data['total_length'] += seq_length
                    data['max_length'] = max(data['max_length'], seq_length)
        
        # Calculate weights
        weights = {}
        for pattern, data in pattern_data.items():
            avg_length = data['total_length'] / data['occurrences']
            weights[pattern] = {
                'weight': avg_length / max_length,
                'avg_length': avg_length,
                'max_length': data['max_length'],
                'occurrences': data['occurrences']
            }
        
        return weights, max_length

def print_weight_analysis(weights):
    """Print formatted weight analysis."""
    print("\nPattern Weight Analysis:")
    print("\nPattern\tWeight\tAvg Length\tMax Length\tOccurrences")
    
    for pattern, data in sorted(weights.items(), key=lambda x: x[1]['weight'], reverse=True):
        print(f"{pattern}\t{data['weight']:.3f}\t{data['avg_length']:.1f}\t"
              f"{data['max_length']}\t{data['occurrences']}")

# Usage example
analyzer = CollatzPatternAnalyzer()
weights, max_length = analyzer.analyze_range(3, 16)
print_weight_analysis(weights)