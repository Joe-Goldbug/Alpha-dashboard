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
ORIG = f"-ts_mean(rank({NET}), 20)"

VARIANTS = [
    # 1. Filter out the non-extreme low
    {"expr": f"trade_when(rank({NET}) < 0.2, {ORIG}, -1)", "decay": 5},
    
    # 2. Filter out the extreme high
    {"expr": f"trade_when(rank({NET}) < 0.8, {ORIG}, -1)", "decay": 5},
    
    # 3. Use 10 days
    {"expr": f"-ts_mean(rank({NET}), 10)", "decay": 5},
    
    # 4. Use 60 days
    {"expr": f"-ts_mean(rank({NET}), 60)", "decay": 5},
    
    # 5. Remove rank inside ts_mean
    {"expr": f"-ts_mean({NET}, 20)", "decay": 5},
    
    # 6. zscore the raw mean
    {"expr": f"-zscore(ts_mean({NET}, 20))", "decay": 5},
    
    # 7. rank the raw mean
    {"expr": f"-rank(ts_mean({NET}, 20))", "decay": 5},
    
    # 8. Add cross-sectional zscore to original
    {"expr": f"zscore({ORIG})", "decay": 5}
]

alpha_list = []
for v in VARIANTS:
    s = settings.copy()
    s["decay"] = v["decay"]
    alpha_list.append({"type": "REGULAR", "settings": s, "regular": v["expr"]})

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "iter7_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} iter7 variants to {out_path}")
