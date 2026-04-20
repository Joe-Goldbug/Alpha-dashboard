import asyncio
import aiohttp
import sys
import os

sys.path.insert(0, '/workspace/WQOS')
from src.sessions.session_client import get_session

FIELD = "oth561_basic_stat_net_buy_user_num"
ALPHAS = [
    f"neutralize(-ts_mean(rank({FIELD}), 20), subindustry)",
    f"-winsorize(ts_mean(rank({FIELD}), 20), std=3)",
    f"-ts_mean(ts_rank({FIELD}, 10), 20)",
    f"-ts_decay_linear(rank({FIELD}), 40)"
]

async def poll_simulation(session, location):
    while True:
        try:
            async with session.get(location) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    status = data.get('status')
                    if status in ['COMPLETE', 'ERROR', 'FAIL', 'WARNING']:
                        if status == 'COMPLETE':
                            alpha_id = data.get('alpha')
                            check_url = f"https://api.worldquantbrain.com/alphas/{alpha_id}/check"
                            async with session.get(check_url) as c_resp:
                                if c_resp.status == 200:
                                    data['check_data'] = await c_resp.json()
                        return data
        except Exception as e:
            pass
        await asyncio.sleep(4)

async def submit_alpha(session, expr):
    payload = {
        "type": "REGULAR",
        "settings": {
            "instrumentType": "EQUITY",
            "region": "CHN",
            "universe": "TOP2000U",
            "delay": 1,
            "decay": 3,
            "neutralization": "SLOW_AND_FAST",
            "truncation": 0.08,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "ON",
            "language": "FASTEXPR",
            "visualization": False,
            "maxTrade": "OFF"
        },
        "regular": expr
    }
    
    try:
        async with session.post('https://api.worldquantbrain.com/simulations', json=payload) as resp:
            if resp.status == 201:
                location = resp.headers.get('Location')
                return await poll_simulation(session, location)
            else:
                return {"status": "SUBMIT_ERROR", "err": await resp.text()}
    except Exception as e:
        return {"status": "EXCEPTION", "err": str(e)}

async def run():
    s = get_session()
    cookie_jar = aiohttp.CookieJar()
    cookie_jar.update_cookies(s.cookies)
    headers = {"Authorization": s.headers.get("Authorization", ""), "Content-Type": "application/json"}
    for k, v in s.headers.items():
        headers[k] = v
        
    async with aiohttp.ClientSession(cookie_jar=cookie_jar, headers=headers) as session:
        tasks = [submit_alpha(session, a) for a in ALPHAS]
        results = await asyncio.gather(*tasks)
        for expr, r in zip(ALPHAS, results):
            if r['status'] == 'COMPLETE':
                is_stats = r.get('is', {})
                checks = r.get('check_data', {}).get('checks', []) if isinstance(r.get('check_data', {}), dict) and 'checks' in r.get('check_data', {}) else []
                fails = [c['name'] for c in checks if c.get('result') == 'FAIL']
                print(f"Expr: {expr}")
                print(f"Margin: {is_stats.get('margin')}, Sharpe: {is_stats.get('sharpe')}, Fails: {fails}\n")
            else:
                print(f"Failed: {expr} - {r}")

if __name__ == '__main__':
    asyncio.run(run())
