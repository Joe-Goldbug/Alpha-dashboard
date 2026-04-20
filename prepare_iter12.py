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
BUY = "oth561_basic_stat_buy_user_num"
ORIG = f"-ts_mean(rank({NET}), 20)"

VARIANTS = [
    # 1. Filter out bottom 50% of retail volume
    {"expr": f"trade_when(rank({BUY}) > 0.5, {ORIG}, -1)", "decay": 5},
    
    # 2. Filter out bottom 80% of retail volume
    {"expr": f"trade_when(rank({BUY}) > 0.8, {ORIG}, -1)", "decay": 5},
    
    # 3. Filter out bottom 30% of retail volume
    {"expr": f"trade_when(rank({BUY}) > 0.3, {ORIG}, -1)", "decay": 5},
    
    # 4. Scale by retail volume
    {"expr": f"{ORIG} * rank({BUY})", "decay": 5},
    
    # 5. Scale by retail volume (inverse)
    {"expr": f"{ORIG} * (1 - rank({BUY}))", "decay": 5},
    
    # 6. Filter bottom 50% on a 20-day mean of retail volume
    {"expr": f"trade_when(ts_mean(rank({BUY}), 20) > 0.5, {ORIG}, -1)", "decay": 5},
    
    # 7. Use median instead of mean
    {"expr": f"-ts_median(rank({NET}), 20)", "decay": 5},
    
    # 8. Use ts_median with filter
    {"expr": f"trade_when(rank({BUY}) > 0.5, -ts_median(rank({NET}), 20), -1)", "decay": 5}
]

alpha_list = []
for v in VARIANTS:
    s = settings.copy()
    s["decay"] = v["decay"]
    alpha_list.append({"type": "REGULAR", "settings": s, "regular": v["expr"]})

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "iter12_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} iter12 variants to {out_path}")
