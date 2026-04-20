import sys, json, os
sys.path.append("/workspace/brain-sim-alphas-batch-track/scripts")
import ace_lib
import requests
with open("/workspace/brain-sim-alphas-batch-track/configs/config.json", "r") as f:
    config = json.load(f)
    os.environ["BRAIN_EMAIL"] = config["email"]
    os.environ["BRAIN_PASSWORD"] = config["password"]
session = ace_lib.start_session()
res = session.get(f"{ace_lib.brain_api_url}/operators")
try:
    ops = res.json()
    names = [op.get("name") for op in ops if op.get("name")]
    print([n for n in names if "winsorize" in n.lower() or "zscore" in n.lower() or "scale" in n.lower()])
except Exception as e:
    print(e)
