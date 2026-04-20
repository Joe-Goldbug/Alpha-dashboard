import sys, json, os
sys.path.append("/workspace/brain-sim-alphas-batch-track/scripts")

import ace_lib
import requests

with open("/workspace/brain-sim-alphas-batch-track/configs/config.json", "r") as f:
    config = json.load(f)
    os.environ["BRAIN_EMAIL"] = config["email"]
    os.environ["BRAIN_PASSWORD"] = config["password"]

session = ace_lib.start_session()
a = "blWbAK8K"
res = session.get(f"{ace_lib.brain_api_url}/alphas/{a}")
print(json.dumps(res.json(), indent=2))
