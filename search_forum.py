import sys, json, os
sys.path.append("/workspace/brain-sim-alphas-batch-track/scripts")

import ace_lib
import requests

with open("/workspace/brain-sim-alphas-batch-track/configs/config.json", "r") as f:
    config = json.load(f)
    os.environ["BRAIN_EMAIL"] = config["email"]
    os.environ["BRAIN_PASSWORD"] = config["password"]

session = ace_lib.start_session()
res = ace_lib.search_forum_posts(session, "LOW_ROBUST_UNIVERSE_SHARPE")
print(json.dumps(res, indent=2)[:2000])
