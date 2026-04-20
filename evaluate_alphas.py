import csv
import os

p = '/data/user/skills/brain-sim-alphas-batch-track/outputs/simulation_status.csv'

if os.path.exists(p):
    print(f"--- Analysis for {p} ---")
    completed_alphas = []
    
    with open(p, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('status') in ['COMPLETE', 'COMPLETED', 'DONE']:
                try:
                    sharpe = float(row.get('sharpe', 0))
                    fitness = float(row.get('fitness', 0))
                    turnover = float(row.get('turnover', 0))
                    returns = float(row.get('returns', 0))
                    margin = float(row.get('margin', 0))
                    
                    completed_alphas.append({
                        'id': row.get('alpha_id', ''),
                        'expr': row.get('regular', ''),
                        'sharpe': sharpe,
                        'abs_sharpe': abs(sharpe),
                        'fitness': fitness,
                        'turnover': turnover,
                        'returns': returns,
                        'margin': margin
                    })
                except ValueError:
                    pass
    
    if completed_alphas:
        print(f"Total COMPLETE alphas: {len(completed_alphas)}")
        
        # Sort by absolute Sharpe
        sorted_alphas = sorted(completed_alphas, key=lambda x: x['abs_sharpe'], reverse=True)
        
        print("\n--- Top Most Competitive Alphas (by |Sharpe|) ---")
        
        # Print header
        print(f"{'Alpha ID':<20} | {'Sharpe':<8} | {'Fitness':<8} | {'Turnover':<8} | {'Returns':<8} | {'Expression'}")
        print("-" * 120)
        
        for a in sorted_alphas[:15]:
            print(f"{a['id']:<20} | {a['sharpe']:>8.2f} | {a['fitness']:>8.2f} | {a['turnover']:>8.4f} | {a['returns']:>8.4f} | {a['expr']}")
    else:
        print("No COMPLETE alphas found in the file.")
else:
    print(f"File not found: {p}")
