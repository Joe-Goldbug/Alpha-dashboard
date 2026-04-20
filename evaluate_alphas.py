import csv
import os

files_to_check = [
    '/data/user/skills/brain-sim-alphas-batch-track/outputs/simulation_status_ppa_final.csv',
    '/data/user/skills/brain-sim-alphas-batch-track/outputs/simulation_status_ppa_v2.csv'
]

for p in files_to_check:
    if os.path.exists(p):
        print(f"--- Analysis for {p} ---")
        completed_alphas = []
        
        with open(p, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('status') == 'COMPLETE':
                    try:
                        sharpe = float(row.get('sharpe', 0))
                        fitness = float(row.get('fitness', 0))
                        turnover = float(row.get('turnover', 0))
                        
                        completed_alphas.append({
                            'id': row.get('alpha_id', ''),
                            'expr': row.get('regular', ''),
                            'sharpe': sharpe,
                            'abs_sharpe': abs(sharpe),
                            'fitness': fitness,
                            'turnover': turnover,
                            'returns': row.get('returns', '')
                        })
                    except ValueError:
                        pass
        
        if completed_alphas:
            print(f"Total COMPLETE alphas: {len(completed_alphas)}")
            
            # Filter and sort
            # Good alphas: Turnover between 1% and 70%
            valid_turnover = [a for a in completed_alphas if 0.01 <= a['turnover'] <= 0.70]
            print(f"Alphas with valid turnover (1%-70%): {len(valid_turnover)}")
            
            # Sort by absolute Sharpe
            sorted_alphas = sorted(valid_turnover, key=lambda x: x['abs_sharpe'], reverse=True)
            
            print(f"Alphas with |Sharpe| > 0.8: {len([a for a in sorted_alphas if a['abs_sharpe'] > 0.8])}")
            print("\n--- Top 10 Most Competitive Alphas (by |Sharpe|) ---")
            
            # Print header
            print(f"{'Alpha ID':<20} | {'Sharpe':<8} | {'Fitness':<8} | {'Turnover':<8} | {'Returns':<8} | {'Expression'}")
            print("-" * 120)
            
            for a in sorted_alphas[:10]:
                print(f"{a['id']:<20} | {a['sharpe']:>8.2f} | {a['fitness']:>8.2f} | {a['turnover']:>8.4f} | {a['returns']:>8} | {a['expr']}")
            
            break # only do the first valid file
