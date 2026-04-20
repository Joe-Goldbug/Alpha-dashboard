import json

ALPHA_TEMPLATES = [
    "-group_zscore({field}, subindustry)",
    "-ts_rank(ts_delta({field}, 5), 20)",
    "-correlation({field}, returns, 20)",
    "({field} - ts_mean({field}, 20)) / (ts_std_dev({field}, 20) + 0.001)",
    "ts_delta(ts_mean({field}, 10), 40)",
    "-signed_power(group_rank({field}, sector) - 0.5, 3)"
]

valid_fields = ['oth561_basic_stat_buy_user_num', 'oth561_basic_stat_sell_user_num', 'oth561_basic_stat_net_buy_user_num']

alpha_list = []
for field in valid_fields:
    for template in ALPHA_TEMPLATES:
        expr = template.format(field=field)
        
        alpha_obj = {
            "type": "REGULAR",
            "settings": {
                "instrumentType": "EQUITY",
                "region": "CHN",
                "universe": "TOP2000U",
                "delay": 1,
                "decay": 3,
                "neutralization": "SUBINDUSTRY",
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

# 确保目录存在
import os
os.makedirs("/data/user/skills/brain-sim-alphas-batch-track/data", exist_ok=True)

with open("/data/user/skills/brain-sim-alphas-batch-track/data/alpha_list.json", "w") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Successfully wrote {len(alpha_list)} alphas to /data/user/skills/brain-sim-alphas-batch-track/data/alpha_list.json")
