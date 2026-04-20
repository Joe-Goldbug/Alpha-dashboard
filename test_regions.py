import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.sessions.session_client import get_session
from src.lib.data_client import get_datasets, get_datafields
import time

s = get_session()
print("尝试在其他地区寻找 other561 数据集...")
for region in ["USA", "CHN", "EUR", "ASI", "GLB"]:
    try:
        df = get_datasets(s, instrument_type="EQUITY", region=region, delay=1, universe="TOP3000")
        if not df.empty:
            matches = df[df['id'] == 'other561']
            if not matches.empty:
                print(f"找到 other561! Region: {region}")
                print(f"覆盖率: {matches.iloc[0].get('coverage')}")
                break
        time.sleep(2)
    except Exception as e:
        print(f"Region {region} error: {e}")
