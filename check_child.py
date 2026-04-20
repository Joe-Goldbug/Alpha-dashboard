import sys, json
sys.path.append("/workspace/brain-sim-alphas-batch-track/scripts")
import ace_lib
session = ace_lib.start_session()
res1 = session.get(f"{ace_lib.brain_api_url}/simulations/QX9nUc9k4OHaLuv1WNUzYC").json()
res2 = session.get(f"{ace_lib.brain_api_url}/simulations/3lN46pAO4IvboQChwRQGEE").json()
print("3: ", res1.get("status"), res1.get("message"))
print("4: ", res2.get("status"), res2.get("message"))
