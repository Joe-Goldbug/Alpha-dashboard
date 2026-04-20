import sys
import os
import aiohttp
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/WQOS'))
from src.sessions.session_client import get_session
import asyncio

async def test():
    s = get_session()
    cookie_jar = aiohttp.CookieJar()
    cookie_jar.update_cookies(s.cookies)
    
    async with aiohttp.ClientSession(cookie_jar=cookie_jar) as session:
        test_neut = ["SLOW_FAST", "SLOW_FAST_FACTORS", "SLOW_AND_FAST_FACTORS", "Slow + Fast factors"]
        for neut in test_neut:
            data = {
                "type": "REGULAR",
                "settings": {
                    "instrumentType": "EQUITY",
                    "region": "USA",
                    "universe": "TOP3000",
                    "delay": 1,
                    "decay": 0,
                    "neutralization": neut,
                    "nanHandling": "ON",
                    "language": "FASTEXPR",
                    "truncation": 0.08,
                    "pasteurization": "ON",
                    "unitHandling": "VERIFY",
                    "maxTrade": "OFF"
                },
                "regular": "close"
            }
            async with session.post('https://api.worldquantbrain.com/simulations', json=data) as resp:
                if resp.status == 400:
                    try:
                        err = await resp.json()
                        print(f"{neut} failed: {err}")
                    except:
                        print(f"{neut} failed: {await resp.text()}")
                elif resp.status in (200, 201):
                    print(f"✅ {neut} succeeded! Location: {resp.headers.get('Location')}")
                else:
                    print(f"Status {resp.status} for {neut}")

asyncio.run(test())
