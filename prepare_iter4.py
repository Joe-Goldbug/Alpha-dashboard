import json
import os

settings = {
    "instrumentType": "EQUITY",
    "region": "CHN",
    "universe": "TOP2000U",
    "delay": 1,
    "decay": 5, # We know decay=5 helps Margin for rank
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
    # 1. scale
    {"expr": f"scale({ORIG})", "decay": 5},
    
    # 2. sign * power
    {"expr": f"sign({ORIG}) * power(abs({ORIG}), 1.5)", "decay": 5},
    
    # 3. trade_when
    {"expr": f"trade_when(rank({NET}) > 0.2, {ORIG}, -1)", "decay": 5},
    {"expr": f"trade_when(rank({NET}) < 0.8, {ORIG}, -1)", "decay": 5},
    
    # 4. winsorize
    {"expr": f"winsorize({ORIG}, std=2)", "decay": 5},
    
    # 5. Sell field instead of Net Buy
    {"expr": f"-ts_mean(rank({SELL}), 20)", "decay": 5},
    {"expr": f"-ts_mean(rank({SELL}), 40)", "decay": 5},
    
    # 6. ts_rank on sell
    {"expr": f"-ts_rank({SELL}, 20)", "decay": 5},
    {"expr": f"-ts_rank({SELL}, 40)", "decay": 5},
    
    # 7. Larger decay to push margin even higher
    {"expr": ORIG, "decay": 10},
    {"expr": f"-ts_mean(rank({NET}), 40)", "decay": 10}
]

alpha_list = []
for v in VARIANTS:
    s = settings.copy()
    s["decay"] = v["decay"]
    alpha_list.append({"type": "REGULAR", "settings": s, "regular": v["expr"]})

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "iter4_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} iter4 variants to {out_path}")
