import sys
import requests
import json
import os

sys.path.insert(0, '/workspace/WQOS')
from src.sessions.session_client import get_session

def main():
    s = get_session()
    alpha_id = "blWbAK8K"
    url = f"https://api.worldquantbrain.com/alphas/{alpha_id}"
    
    resp = s.get(url)
    if resp.status_code == 200:
        data = resp.json()
        print("--- Alpha Details ---")
        print(f"ID: {data.get('id')}")
        
        expr = data.get('regular', data.get('regular_expression', 'N/A'))
        # If 'regular' is not direct string, it might be nested or we just use 'regular' field.
        if isinstance(expr, str) and not expr.strip() and 'regular' in data:
            pass # fallback to something else if needed
            
        # some versions have regular inside 'settings'? No, it's at root level.
        print(f"Expression: {expr}")
        
        settings = data.get('settings', {})
        print(f"Region: {settings.get('region')}")
        print(f"Universe: {settings.get('universe')}")
        print(f"Delay: {settings.get('delay')}")
        print(f"Neutralization: {settings.get('neutralization')}")
        print(f"Decay: {settings.get('decay')}")
        
        is_stats = data.get('is', {})
        print("--- Metrics ---")
        print(f"Sharpe: {is_stats.get('sharpe')}")
        print(f"Fitness: {is_stats.get('fitness')}")
        print(f"Turnover: {is_stats.get('turnover')}")
        print(f"Margin: {is_stats.get('margin')}")
        print(f"Returns: {is_stats.get('returns')}")
        
        check_url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/check"
        check_resp = s.get(check_url)
        print("--- Submission Checks ---")
        if check_resp.status_code == 200:
            checks = check_resp.json()
            # It might be a dict with 'checks' or just the checks
            if isinstance(checks, dict) and 'checks' in checks:
                check_list = checks['checks']
            else:
                check_list = checks
            if isinstance(check_list, list):
                for c in check_list:
                    print(f"Check {c.get('name')}: {c.get('result')} - {c.get('details', '')}")
            else:
                print(f"Check data: {checks}")
        else:
            print(f"No check response: {check_resp.status_code} {check_resp.text}")
    else:
        print(f"Failed to get alpha details for {alpha_id}: {resp.status_code} {resp.text}")

if __name__ == '__main__':
    main()
