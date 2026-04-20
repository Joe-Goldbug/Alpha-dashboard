import sys
import os
import asyncio
import json

sys.path.insert(0, '/workspace/WQOS')
from src.sessions.session_client import get_session
import aiohttp

async def fetch_alpha(alpha_id):
    s = get_session()
    cookie_jar = aiohttp.CookieJar()
    cookie_jar.update_cookies(s.cookies)
    async with aiohttp.ClientSession(cookie_jar=cookie_jar, headers=s.headers) as session:
        url = f"https://api.worldquantbrain.com/alphas/{alpha_id}"
        async with session.get(url) as resp:
            if resp.status == 200:
                return await resp.json()
            else:
                return {"error": await resp.text()}

async def run():
    alpha_id = "blWbAK8K"
    data = await fetch_alpha(alpha_id)
    if 'regular' in data:
        print("Expression:", data['regular'])
        print("Settings:", data['settings'])
        is_data = data.get('is', {})
        print("IS Sharpe:", is_data.get('sharpe'))
        print("IS Fitness:", is_data.get('fitness'))
        print("IS Margin:", is_data.get('margin'))
        print("IS Turnover:", is_data.get('turnover'))
        checks = data.get('checks', [])
        for chk in checks:
            print("Check:", chk.get('name'), "->", chk.get('result'))
    else:
        print("Could not fetch alpha details:", data)

asyncio.run(run())
