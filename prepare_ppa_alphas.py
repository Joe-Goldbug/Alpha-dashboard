import json
import os

buy = "oth561_basic_stat_buy_user_num"
sell = "oth561_basic_stat_sell_user_num"
net = "oth561_basic_stat_net_buy_user_num"

expressions = [
    f"-rank(ts_delta({buy}, 5))",
    f"-rank(ts_delta({sell}, 5))",
    f"-rank(ts_delta({net}, 5))",
    f"-ts_rank({buy}, 20)",
    f"-ts_rank({sell}, 20)",
    f"-ts_rank({net}, 20)",
    f"-group_rank(ts_mean({buy}, 5), subindustry)",
    f"-group_rank(ts_mean({sell}, 5), subindustry)",
    f"-group_rank(ts_mean({net}, 5), subindustry)",
    f"({buy} - ts_mean({buy}, 10)) / (ts_std_dev({buy}, 10) + 0.001)",
    f"({sell} - ts_mean({sell}, 10)) / (ts_std_dev({sell}, 10) + 0.001)",
    f"({net} - ts_mean({net}, 10)) / (ts_std_dev({net}, 10) + 0.001)",
    f"({buy} - {sell}) / ({buy} + {sell} + 1)",
    f"-rank(({buy} - {sell}) / ({buy} + {sell} + 1))",
    f"ts_delta(({buy} - {sell}) / ({buy} + {sell} + 1), 3)",
    f"-rank(ts_delta(({buy} - {sell}) / ({buy} + {sell} + 1), 3))",
    f"-signed_power(ts_delta({net}, 3), 2)",
    f"-signed_power(ts_delta({buy}, 3), 2)",
]

neutralization = "SLOW_AND_FAST"

alpha_list = []
for expr in expressions:
    alpha_obj = {
        "type": "REGULAR",
        "settings": {
            "instrumentType": "EQUITY",
            "region": "CHN",
            "universe": "TOP2000U",
            "delay": 1,
            "decay": 3,
            "neutralization": neutralization,
            "truncation": 0.08,
            "pasteurization": "ON",
            "unitHandling": "VERIFY",
            "nanHandling": "ON",
            "language": "FASTEXPR",
            "visualization": False,
            "maxTrade": "OFF",
        },
        "regular": expr,
    }
    alpha_list.append(alpha_obj)

os.makedirs("/data/user/skills/brain-sim-alphas-batch-track/data", exist_ok=True)

with open("/data/user/skills/brain-sim-alphas-batch-track/data/alpha_list_ppa.json", "w") as f:
    json.dump(alpha_list, f, indent=2)

print(f"Wrote {len(alpha_list)} PPA alphas")
