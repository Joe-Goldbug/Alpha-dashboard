import json
import os

settings = {
    "instrumentType": "EQUITY",
    "region": "CHN",
    "universe": "TOP2000U",
    "delay": 1,
    "decay": 5, 
    "neutralization": "SLOW_AND_FAST",
    "truncation": 0.08,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "language": "FASTEXPR",
    "visualization": False,
    "maxTrade": "OFF"
}

NET = "oth561_basic_stat_net_buy_user_num"
BUY_P = "oth561_basic_stat_buy_rebalancing_price_avg"
SELL_P = "oth561_basic_stat_sell_rebalancing_price_avg"

VARIANTS = [
    {"expr": f"-ts_mean(rank({BUY_P} / ({SELL_P} + 1)), 20)", "decay": 5},
    {"expr": f"trade_when({BUY_P} > {SELL_P}, -ts_mean(rank({NET}), 20), -1)", "decay": 5},
    {"expr": f"-ts_mean(rank({NET}), 60)", "decay": 5},
    {"expr": f"-ts_mean(rank({NET}), 100)", "decay": 5},
    {"expr": f"-ts_decay_linear(rank({NET}), 60)", "decay": 5},
    {"expr": f"ts_mean(rank({SELL_P}), 20)", "decay": 5},
    {"expr": f"-ts_mean(rank({BUY_P}), 20)", "decay": 5},
    {"expr": f"trade_when({NET} < 0, -ts_mean(rank({NET}), 20), -1)", "decay": 5}
]

alpha_list = []
for v in VARIANTS:
    s = settings.copy()
    s["decay"] = v["decay"]
    alpha_list.append({"type": "REGULAR", "settings": s, "regular": v["expr"]})

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "iter10_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} iter10 variants to {out_path}")
