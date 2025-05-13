import time
import json
import random

def simple_ranking(items):
    """A simple ranking algorithm that sorts items by their score."""
    start_time = time.time()
    
    # Sort items by score in descending order
    ranked_items = sorted(items, key=lambda x: x['score'], reverse=True)
    
    # Assign ranks
    for i, item in enumerate(ranked_items):
        item['rank'] = i + 1
    
    end_time = time.time()
    return ranked_items, end_time - start_time

def optimized_ranking(items):
    """An optimized ranking algorithm that pre-computes scores and uses a more efficient sorting method."""
    start_time = time.time()
    
    # Create a list of (score, index) tuples for faster sorting
    scores_with_indices = [(item['score'], i) for i, item in enumerate(items)]
    
    # Sort the scores (this is faster than sorting the full items)
    scores_with_indices.sort(reverse=True)
    
    # Create a new list with the sorted items and assign ranks
    ranked_items = []
    for rank, (_, index) in enumerate(scores_with_indices, 1):
        item = items[index].copy()  # Create a copy to avoid modifying the original
        item['rank'] = rank
        ranked_items.append(item)
    
    end_time = time.time()
    return ranked_items, end_time - start_time

def elo_ranking(items, k_factor=32):
    """Implements an ELO-like ranking system through simulated matches."""
    start_time = time.time()
    
    # Initialize ELO scores
    for item in items:
        item['elo'] = 1000  # Starting ELO score
    
    # Simulate matches between items based on their scores
    num_matches = len(items) * 5  # Number of matches to simulate
    
    for _ in range(num_matches):
        # Select two random items for a match
        item_a, item_b = random.sample(items, 2)
        
        # Calculate expected scores
        expect_a = 1 / (1 + 10**((item_b['score'] - item_a['score']) / 50))
        expect_b = 1 - expect_a
        
        # Update ELO scores based on actual outcome (determined by original score)
        if item_a['score'] > item_b['score']:
            outcome_a, outcome_b = 1, 0
        elif item_a['score'] < item_b['score']:
            outcome_a, outcome_b = 0, 1
        else:
            outcome_a, outcome_b = 0.5, 0.5
        
        item_a['elo'] += k_factor * (outcome_a - expect_a)
        item_b['elo'] += k_factor * (outcome_b - expect_b)
    
    # Sort items by ELO score
    ranked_items = sorted(items, key=lambda x: x['elo'], reverse=True)
    
    # Assign ranks
    for i, item in enumerate(ranked_items):
        item['rank'] = i + 1
    
    end_time = time.time()
    return ranked_items, end_time - start_time

def generate_sample_data(n=1000):
    """Generate sample data for testing the ranking algorithms."""
    items = []
    for i in range(n):
        items.append({
            'id': i,
            'name': f'Item {i}',
            'score': random.uniform(0, 100)
        })
    return items

def main():
    # Generate sample data
    data = generate_sample_data(1000)
    
    # Apply simple ranking
    simple_data, simple_time = simple_ranking([item.copy() for item in data])
    print(f"Simple ranking completed in {simple_time:.6f} seconds")
    
    # Apply optimized ranking
    optimized_data, optimized_time = optimized_ranking([item.copy() for item in data])
    print(f"Optimized ranking completed in {optimized_time:.6f} seconds")
    print(f"Optimization improvement: {(simple_time - optimized_time) / simple_time * 100:.2f}%")
    
    # Apply ELO ranking
    elo_data, elo_time = elo_ranking([item.copy() for item in data])
    print(f"ELO ranking completed in {elo_time:.6f} seconds")
    
    # Save results to JSON file
    results = {
        'algorithms': [
            {
                'name': 'Simple Ranking',
                'execution_time': simple_time,
                'ranked_items': simple_data[:10],  # Only include top 10 for brevity
            },
            {
                'name': 'Optimized Ranking',
                'execution_time': optimized_time,
                'ranked_items': optimized_data[:10],
            },
            {
                'name': 'ELO Ranking',
                'execution_time': elo_time,
                'ranked_items': elo_data[:10],
            }
        ],
        'total_items': len(data),
        'performance_comparison': {
            'simple_vs_optimized': {
                'time_difference': simple_time - optimized_time,
                'percentage_improvement': (simple_time - optimized_time) / simple_time * 100
            },
            'simple_vs_elo': {
                'time_difference': simple_time - elo_time,
                'percentage_improvement': (simple_time - elo_time) / simple_time * 100
            }
        }
    }
    
    # Save to JSON file
    with open('ranking_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to 'ranking_results.json'")

if __name__ == "__main__":
    main()
