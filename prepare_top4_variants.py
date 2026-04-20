import json
import os

settings = {
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
    "maxTrade": "OFF",
}

sell = "oth561_basic_stat_sell_user_num"
net = "oth561_basic_stat_net_buy_user_num"

exprs = [
    "ts_rank({sell}, 20)",
    "ts_rank({sell}, 60)",
    "ts_rank(ts_mean({sell}, 5), 60)",
    "ts_rank(ts_mean({sell}, 10), 80)",

    "({net} - ts_mean({net}, 10)) / (ts_std_dev({net}, 10) + 0.001)",
    "({net} - ts_mean({net}, 20)) / (ts_std_dev({net}, 20) + 0.001)",
    "ts_decay_linear(({net} - ts_mean({net}, 20)) / (ts_std_dev({net}, 20) + 0.001), 5)",
    "ts_decay_linear(({net} - ts_mean({net}, 40)) / (ts_std_dev({net}, 40) + 0.001), 10)",

    "signed_power(ts_delta({net}, 5), 2)",
    "signed_power(ts_delta({net}, 10), 2)",
    "ts_decay_linear(signed_power(ts_delta({net}, 10), 2), 5)",
]

exprs = [e.format(sell=sell, net=net) for e in exprs]

alpha_list = []
for e in exprs:
    alpha_list.append({"type": "REGULAR", "settings": settings, "regular": e})

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "top4_variants.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2, ensure_ascii=False)

print(out_path)
print(len(alpha_list))
