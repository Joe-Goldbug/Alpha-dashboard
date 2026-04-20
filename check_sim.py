import sys, json, os
sys.path.append("/workspace/brain-sim-alphas-batch-track/scripts")
with open("/workspace/brain-sim-alphas-batch-track/configs/config.json", "r") as f:
    config = json.load(f)
    os.environ["BRAIN_EMAIL"] = config["email"]
    os.environ["BRAIN_PASSWORD"] = config["password"]

import ace_lib
import requests

session = ace_lib.start_session()
res = session.get(f"{ace_lib.brain_api_url}/simulations/1tp3gncdQ4EjbuFj7dWsCDo")
print(json.dumps(res.json(), indent=2))
