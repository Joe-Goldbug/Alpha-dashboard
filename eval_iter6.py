import csv
import sys

def parse_float(v):
    try:
        return float(v)
    except:
        return 0.0

alphas = []
with open('/workspace/brain-sim-alphas-batch-track/outputs/simulation_status_iter6.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row['status'] in ['COMPLETED', 'COMPLETE']:
            alphas.append({
                'id': row['alpha_id'],
                'expr': row['regular_expression'],
                'sharpe': parse_float(row['sharpe']),
                'fitness': parse_float(row['fitness']),
                'turnover': parse_float(row['turnover']),
                'margin': parse_float(row.get('margin', 0)),
                'error': row.get('error', ''),
                'error_details': row.get('error_details', '')
            })

alphas.sort(key=lambda x: x['sharpe'], reverse=True)

print("Top 3 Alphas (Iter 6):")
for a in alphas[:3]:
    print(f"Alpha: {a['id']} | Sharpe: {a['sharpe']} | Fitness: {a['fitness']} | TO: {a['turnover']} | Expr: {a['expr']}")
    print(f"  Error: {a['error_details']}")
