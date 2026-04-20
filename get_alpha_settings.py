import sys
import requests
sys.path.insert(0, '/workspace/WQOS')
from src.sessions.session_client import get_session

def main():
    s = get_session()
    alpha_id = "blWbAK8K"
    url = f"https://api.worldquantbrain.com/alphas/{alpha_id}"
    resp = s.get(url)
    if resp.status_code == 200:
        data = resp.json()
        print(data.get('settings'))
if __name__ == '__main__':
    main()
