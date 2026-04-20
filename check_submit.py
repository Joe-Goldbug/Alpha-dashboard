import sys, json, os
sys.path.append("/workspace/brain-sim-alphas-batch-track/scripts")

import ace_lib
import requests

with open("/workspace/brain-sim-alphas-batch-track/configs/config.json", "r") as f:
    config = json.load(f)
    os.environ["BRAIN_EMAIL"] = config["email"]
    os.environ["BRAIN_PASSWORD"] = config["password"]

session = ace_lib.start_session()
res = session.get(f"{ace_lib.brain_api_url}/alphas/58qgOVjJ/check")
data = res.json()
for check in data.get("is", {}).get("checks", []):
    if check.get("name") == "LOW_ROBUST_UNIVERSE_SHARPE.WITH_RATIO":
        print(f"Robust Universe Sharpe: {check.get('value')} (limit: {check.get('limit')})")
