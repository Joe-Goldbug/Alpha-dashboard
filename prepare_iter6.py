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
SELL = "oth561_basic_stat_sell_user_num"

ORIG = f"-ts_mean(rank({NET}), 20)"

VARIANTS = [
    # Filter weak signals
    {"expr": f"trade_when(rank({NET}) > 0.5, {ORIG}, -1)", "decay": 5},
    {"expr": f"trade_when(rank({NET}) > 0.8, {ORIG}, -1)", "decay": 5},
    {"expr": f"trade_when({SELL} > 0, {ORIG}, -1)", "decay": 5},
    
    # Scale and power to emphasize extreme values
    {"expr": f"sign({ORIG}) * power(abs({ORIG}), 1.5)", "decay": 5},
    {"expr": f"scale({ORIG})", "decay": 5},
    
    # ts_decay_linear
    {"expr": f"-ts_decay_linear(rank({NET}), 20)", "decay": 5},
    
    # zscore
    {"expr": f"-ts_mean(zscore({NET}), 20)", "decay": 5},
    
    # group_rank by subindustry if allowed
    {"expr": f"-ts_mean(group_rank({NET}, subindustry), 20)", "decay": 5}
]

alpha_list = []
for v in VARIANTS:
    s = settings.copy()
    s["decay"] = v["decay"]
    alpha_list.append({"type": "REGULAR", "settings": s, "regular": v["expr"]})

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "iter6_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} iter6 variants to {out_path}")
