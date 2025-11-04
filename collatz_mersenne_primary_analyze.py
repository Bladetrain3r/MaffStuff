def analyze_mersenne_properties(start_k=3, end_k=10):
    results = []
    for k in range(start_k, end_k + 1):
        # Generate Mersenne number and its full binary length cohort
        mersenne = 2**k - 1
        max_number = 2**(k+1) - 1
        
        # Track sequence lengths for all numbers of this length
        lengths = []
        trajectories = []
        
        # Sample numbers of same binary length
        for n in range(2**k, max_number + 1):
            path = track_single_path(n)
            lengths.append(len(path))
            
            # Calculate bounding box of trajectory
            if len(path) > 0:
                m_coords = path[:, 1]  # M-distance
                l_coords = path[:, 2]  # L-distance
                trajectories.append({
                    'number': n,
                    'm_bounds': (min(m_coords), max(m_coords)),
                    'l_bounds': (min(l_coords), max(l_coords))
                })
        
        # Get Mersenne trajectory
        mersenne_path = track_single_path(mersenne)
        
        results.append({
            'k': k,
            'mersenne': mersenne,
            'mersenne_length': len(mersenne_path),
            'max_other_length': max(lengths),
            'mean_length': np.mean(lengths),
            'is_maximum': len(mersenne_path) >= max(lengths),
            'trajectory_bounds': trajectories
        })
    
    return results

results = analyze_mersenne_properties(3, 10)

for result in results:
    print(f"K: {result['k']}, Mersenne: {result['mersenne']}, Mersenne Length: {result['mersenne_length']}, Max Other Length: {result['max_other_length']}, Mean Length: {result['mean_length']}, Is Maximum: {result['is_maximum']}")