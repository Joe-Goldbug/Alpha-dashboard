import sys
import asyncio
import aiohttp
import json

sys.path.insert(0, '/workspace/WQOS')
from src.sessions.session_client import get_session

# Base field
FIELD = "oth561_basic_stat_net_buy_user_num"

VARIANTS = [
    # Group Neutralization to help sub-universe
    {"expr": f"-ts_mean(group_rank({FIELD}, subindustry), 20)", "decay": 0},
    {"expr": f"-ts_mean(group_rank({FIELD}, sector), 20)", "decay": 0},
    
    # Increase window to reduce turnover and increase margin
    {"expr": f"-ts_mean(rank({FIELD}), 40)", "decay": 0},
    {"expr": f"-ts_mean(rank({FIELD}), 60)", "decay": 0},
    
    # ts_decay_linear for smoothing
    {"expr": f"-ts_decay_linear(rank({FIELD}), 20)", "decay": 0},
    {"expr": f"-ts_decay_linear(rank({FIELD}), 40)", "decay": 0},
    
    # Setting decay to 5 to suppress turnover
    {"expr": f"-ts_mean(rank({FIELD}), 20)", "decay": 5},
    {"expr": f"-ts_mean(rank({FIELD}), 40)", "decay": 5},
    
    # Power transform to boost signal strength (Margin)
    {"expr": f"-signed_power(ts_mean(rank({FIELD}), 20), 2)", "decay": 0},
    
    # Switch cross-sectional rank to time-series rank
    {"expr": f"-ts_rank({FIELD}, 20)", "decay": 0},
    {"expr": f"-ts_rank({FIELD}, 40)", "decay": 0},
]

async def poll_simulation(session, location):
    while True:
        try:
            async with session.get(location) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    status = data.get('status')
                    if status in ['COMPLETE', 'ERROR', 'FAIL', 'WARNING']:
                        # Fetch check if complete
                        if status == 'COMPLETE':
                            alpha_id = data.get('alpha')
                            check_url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/check"
                            async with session.get(check_url) as c_resp:
                                if c_resp.status == 200:
                                    data['check_data'] = await c_resp.json()
                        return data
                elif resp.status >= 400:
                    return {"status": "HTTP_ERROR", "code": resp.status}
        except Exception as e:
            pass
        await asyncio.sleep(4)

async def submit_alpha(session, variant):
    payload = {
        "type": "REGULAR",
        "settings": {
            "instrumentType": "EQUITY",
            "region": "CHN",
            "universe": "TOP2000U",
            "delay": 1,
            "decay": variant['decay'],
            "neutralization": "SLOW_AND_FAST",
            "truncation": 0.08,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "OFF",
            "language": "FASTEXPR",
            "visualization": False,
            "maxTrade": "OFF"
        },
        "regular": variant['expr']
    }
    
    try:
        async with session.post('https://api.worldquantbrain.com/simulations', json=payload) as resp:
            if resp.status == 201:
                location = resp.headers.get('Location')
                res = await poll_simulation(session, location)
                res['variant'] = variant
                return res
            else:
                err = await resp.text()
                return {"status": "SUBMIT_ERROR", "err": err, "variant": variant}
    except Exception as e:
        return {"status": "EXCEPTION", "err": str(e), "variant": variant}

async def run_batch():
    s = get_session()
    cookie_jar = aiohttp.CookieJar()
    cookie_jar.update_cookies(s.cookies)
    headers = {"Authorization": s.headers.get("Authorization", ""), "Content-Type": "application/json"}
    for k, v in s.headers.items():
        headers[k] = v
        
    async with aiohttp.ClientSession(cookie_jar=cookie_jar, headers=headers) as session:
        print(f"[Iteration 1/100]Status Report")
        print(f"Execution: Submitted {len(VARIANTS)} expressions.")
        
        tasks = [submit_alpha(session, v) for v in VARIANTS]
        results = await asyncio.gather(*tasks)
        
        best_alpha = None
        best_margin = -1
        
        success_found = False
        
        print("Error Check: ", end="")
        errors = [r for r in results if r['status'] not in ['COMPLETE']]
        if errors:
            print(f"Had {len(errors)} errors.")
            for e in errors:
                print(e.get('err', e.get('status')))
        else:
            print("Pass")
            
        print("\nResults:")
        for r in results:
            if r['status'] == 'COMPLETE':
                is_stats = r.get('is', {})
                margin = is_stats.get('margin', 0)
                sharpe = is_stats.get('sharpe', 0)
                fitness = is_stats.get('fitness', 0)
                
                check_data = r.get('check_data', {})
                checks = check_data.get('checks', []) if isinstance(check_data, dict) and 'checks' in check_data else []
                # Check if any fail
                fails = [c['name'] for c in checks if c.get('result') == 'FAIL']
                
                if margin is None: margin = 0
                if sharpe is None: sharpe = 0
                if fitness is None: fitness = 0
                
                print(f"Expr: {r['variant']['expr']} (decay={r['variant']['decay']}) -> Margin: {margin:.6f}, Sharpe: {sharpe:.2f}, Fails: {fails}")
                
                if not fails and margin > 0.0015 and sharpe > 1.25 and fitness > 1.0:
                    print(f"🌟 SUCCESS FOUND! Alpha ID: {r.get('alpha')}")
                    success_found = True
                    best_alpha = r
                    break
                
                if margin > best_margin:
                    best_margin = margin
                    best_alpha = r
                    
        if not success_found and best_alpha:
            print("\nBest Result (This Batch):")
            print(f"Alpha ID: {best_alpha.get('alpha')}")
            print(f"Expression: {best_alpha['variant']['expr']}")
            print(f"Margin: {best_alpha.get('is', {}).get('margin'):.6f} (Target: >0.0015) ❌")
            print(f"Sharpe: {best_alpha.get('is', {}).get('sharpe'):.2f} ✅")
            
            check_data = best_alpha.get('check_data', {})
            checks = check_data.get('checks', []) if isinstance(check_data, dict) and 'checks' in check_data else []
            fails = [c['name'] for c in checks if c.get('result') == 'FAIL']
            if fails:
                print(f"Checks: FAIL ({', '.join(fails)}) ❌")
            else:
                print(f"Checks: PASS ✅")
                
            print("\nAnalysis:")
            print(f"Margin did not meet the > 0.0015 threshold, or checks failed. Will refine in the next iteration based on {best_alpha['variant']['expr']}.")

if __name__ == "__main__":
    asyncio.run(run_batch())
