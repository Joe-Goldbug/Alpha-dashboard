import sys
import os
import asyncio

sys.path.insert(0, '/workspace/WQOS')
from src.sessions.session_client import get_session
from src.lib.simulation.core.session_manager import UnifiedSessionManager

async def fetch_alpha():
    manager = UnifiedSessionManager()
    await manager.initialize()
    s = get_session()
    manager.session.cookie_jar.update_cookies(s.cookies)
    manager.session.headers.update(s.headers)

    alpha_id = "blWbAK8K"
    url = f"https://api.worldquantbrain.com/alphas/{alpha_id}"
    resp = await manager.get(url)
    
    if resp and 'regular' in resp:
        print(f"Alpha Expression: {resp.get('regular')}")
        print(f"Settings: {resp.get('settings')}")
        is_stats = resp.get('is', {})
        print(f"Sharpe: {is_stats.get('sharpe')}")
        print(f"Fitness: {is_stats.get('fitness')}")
        print(f"Margin: {is_stats.get('margin')}")
        print(f"Turnover: {is_stats.get('turnover')}")
    else:
        print(f"Failed to fetch alpha or unexpected response: {resp}")
        
    await manager.close()

asyncio.run(fetch_alpha())
