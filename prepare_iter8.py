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
    # 1. winsorize
    {"expr": f"winsorize({ORIG})", "decay": 5},
    
    # 2. filter 0s
    {"expr": f"trade_when({NET} != 0, {ORIG}, -1)", "decay": 5},
    
    # 3. ts_zscore
    {"expr": f"-ts_zscore(rank({NET}), 20)", "decay": 5},
    
    # 4. ts_scale
    {"expr": f"ts_scale(-ts_mean(rank({NET}), 20), 20)", "decay": 5},
    
    # 5. trade_when sell > 0.5
    {"expr": f"trade_when(rank({SELL}) > 0.5, {ORIG}, -1)", "decay": 5},
    
    # 6. trade_when sell < 0.5
    {"expr": f"trade_when(rank({SELL}) < 0.5, {ORIG}, -1)", "decay": 5},
    
    # 7. winsorize inside
    {"expr": f"-ts_mean(winsorize({NET}), 20)", "decay": 5},
    
    # 8. rank winsorize
    {"expr": f"-ts_mean(rank(winsorize({NET})), 20)", "decay": 5}
]

alpha_list = []
for v in VARIANTS:
    s = settings.copy()
    s["decay"] = v["decay"]
    alpha_list.append({"type": "REGULAR", "settings": s, "regular": v["expr"]})

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "iter8_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} iter8 variants to {out_path}")
