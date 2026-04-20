import asyncio
import aiohttp
import sys
import os

sys.path.insert(0, '/workspace/WQOS')
from src.sessions.session_client import get_session

ALPHAS = [
    "- (oth561_basic_stat_net_buy_user_num - ts_mean(oth561_basic_stat_net_buy_user_num, 10)) / (ts_std_dev(oth561_basic_stat_net_buy_user_num, 10) + 0.001)",
    "-ts_rank(oth561_basic_stat_sell_user_num, 20)",
    "-group_rank(ts_mean(oth561_basic_stat_buy_user_num, 5), subindustry)",
    "-signed_power(ts_delta(oth561_basic_stat_net_buy_user_num, 5), 2)"
]

async def poll_simulation(session, location):
    print(f"Polling {location} ...")
    while True:
        try:
            async with session.get(location) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    status = data.get('status')
                    if status in ['COMPLETE', 'ERROR', 'FAIL', 'WARNING']:
                        return data
                elif resp.status >= 400:
                    return {"status": "HTTP_ERROR", "code": resp.status}
        except Exception as e:
            print(f"Polling error: {e}")
        await asyncio.sleep(3)

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
                print(f"✅ Submitted: {expr[:30]}...")
                return await poll_simulation(session, location)
            else:
                err = await resp.text()
                print(f"❌ Failed to submit {expr[:30]}... : {resp.status} - {err}")
                return {"status": "SUBMIT_ERROR"}
    except Exception as e:
        print(f"❌ Submit exception: {e}")
        return {"status": "EXCEPTION"}

async def run_simulations():
    s = get_session()
    cookie_jar = aiohttp.CookieJar()
    cookie_jar.update_cookies(s.cookies)
    
    headers = {
        "Authorization": s.headers.get("Authorization", ""),
        "Content-Type": "application/json"
    }
    # Update headers from session if present
    for k, v in s.headers.items():
        headers[k] = v
        
    async with aiohttp.ClientSession(cookie_jar=cookie_jar, headers=headers) as session:
        tasks = [submit_alpha(session, expr) for expr in ALPHAS]
        results = await asyncio.gather(*tasks)
        
        print("\n" + "="*80)
        print("🎯 FINAL SIMULATION RESULTS (CHN | TOP2000U | Delay=1 | SLOW_AND_FAST)")
        print("="*80)
        
        for expr, res in zip(ALPHAS, results):
            status = res.get('status')
            print(f"\n💡 Expression: {expr}")
            print(f"Status: {status}")
            
            if status == 'COMPLETE':
                is_stats = res.get('is', {})
                sharpe = is_stats.get('sharpe', 'N/A')
                fitness = is_stats.get('fitness', 'N/A')
                turnover = is_stats.get('turnover', 'N/A')
                alpha_id = res.get('alpha')
                
                print(f"Alpha ID : {alpha_id}")
                print(f"Sharpe   : {sharpe}")
                print(f"Fitness  : {fitness}")
                print(f"Turnover : {turnover}")
                
                # Check negative sharpe advice
                if sharpe != 'N/A' and float(sharpe) < 0:
                    print("⚠️ 提示: Sharpe为负，在公式前去掉或加上负号即可翻转为正信号！")
                
                # Check Turnover advice
                if turnover != 'N/A':
                    t = float(turnover)
                    if t > 0.7:
                        print("⚠️ 提示: Turnover偏高 (>0.7)，建议将 ts_rank 或 ts_mean 的周期拉长。")
                    elif t < 0.01:
                        print("⚠️ 提示: Turnover过低 (<0.01)，信号可能过于稀疏。")
            else:
                print(f"Details: {res}")

if __name__ == "__main__":
    asyncio.run(run_simulations())
