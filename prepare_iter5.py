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
    # 1. Neutralize
    {"expr": f"neutralize({ORIG}, subindustry)", "decay": 5},
    {"expr": f"neutralize({ORIG}, sector)", "decay": 5},
    
    # 2. scale and neutralize
    {"expr": f"scale(neutralize({ORIG}, subindustry))", "decay": 5},
    
    # 3. Use trade_when to filter small values (more aggressively)
    {"expr": f"trade_when(rank({NET}) > 0.5, {ORIG}, -1)", "decay": 5},
    {"expr": f"trade_when(rank({NET}) > 0.8, {ORIG}, -1)", "decay": 5},
    
    # 4. Use different pasteurization/truncation? Wait, PPA rules... 
    # Let's try combining SELL and NET
    {"expr": f"trade_when({SELL} > 0, {ORIG}, -1)", "decay": 5},
    
    # 5. Maybe ts_decay_linear over the neutralized
    {"expr": f"neutralize(-ts_decay_linear(rank({NET}), 20), subindustry)", "decay": 5},
    
    # 6. zscore inside
    {"expr": f"-ts_mean(zscore({NET}), 20)", "decay": 5}
]

alpha_list = []
for v in VARIANTS:
    s = settings.copy()
    s["decay"] = v["decay"]
    alpha_list.append({"type": "REGULAR", "settings": s, "regular": v["expr"]})

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "iter5_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} iter5 variants to {out_path}")
