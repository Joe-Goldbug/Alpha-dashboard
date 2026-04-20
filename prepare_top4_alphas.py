import json
import os

ALPHAS = [
    "- (oth561_basic_stat_net_buy_user_num - ts_mean(oth561_basic_stat_net_buy_user_num, 10)) / (ts_std_dev(oth561_basic_stat_net_buy_user_num, 10) + 0.001)",
    "-ts_rank(oth561_basic_stat_sell_user_num, 20)",
    "-group_rank(ts_mean(oth561_basic_stat_buy_user_num, 5), subindustry)",
    "-signed_power(ts_delta(oth561_basic_stat_net_buy_user_num, 5), 2)"
]

alpha_list = []
for expr in ALPHAS:
    alpha_obj = {
        "type": "REGULAR",
        "settings": {
            "instrumentType": "EQUITY",
            "region": "CHN",
            "universe": "TOP2000U",
            "delay": 1,
            "decay": 3,
            "neutralization": "SLOW_AND_FAST",
            "truncation": 0.08,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "ON",
            "language": "FASTEXPR",
            "visualization": False,
            "maxTrade": "OFF"
        },
        "regular": expr
    }
    alpha_list.append(alpha_obj)

os.makedirs("/data/user/skills/brain-sim-alphas-batch-track/data", exist_ok=True)
out_path = "/data/user/skills/brain-sim-alphas-batch-track/data/top4_alphas.json"

with open(out_path, "w") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} top PPA alphas to {out_path}")
