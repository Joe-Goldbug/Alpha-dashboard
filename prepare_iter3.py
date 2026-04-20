import json
import os

settings = {
    "instrumentType": "EQUITY",
    "region": "CHN",
    "universe": "TOP2000U",
    "delay": 1,
    "decay": 0,
    "neutralization": "SLOW_AND_FAST",
    "truncation": 0.08,
    "pasteurization": "ON",
    "unitHandling": "VERIFY",
    "nanHandling": "OFF",
    "language": "FASTEXPR",
    "visualization": False,
    "maxTrade": "OFF"
}

FIELD = "oth561_basic_stat_net_buy_user_num"
ORIG = f"-ts_mean(rank({FIELD}), 20)"

VARIANTS = [
    # 1. Add decay to settings
    {"expr": ORIG, "decay": 3},
    {"expr": ORIG, "decay": 5},
    
    # 2. Smooth more
    {"expr": f"-ts_mean(rank({FIELD}), 40)", "decay": 0},
    {"expr": f"-ts_decay_linear(ts_mean(rank({FIELD}), 20), 10)", "decay": 0},
    
    # 3. Z-Score cross-sectional instead of rank
    {"expr": f"-ts_mean(zscore({FIELD}), 20)", "decay": 0},
    
    # 4. Cap the rank
    {"expr": f"-ts_mean(cap(rank({FIELD}), 0.1, 0.9), 20)", "decay": 0},
    
    # 5. Use ts_rank instead of rank
    {"expr": f"-ts_mean(ts_rank({FIELD}, 10), 20)", "decay": 0},
    
    # 6. Apply signed_power
    {"expr": f"-signed_power(ts_mean(rank({FIELD}), 20), 2)", "decay": 0},
    
    # 7. Neutralize the rank
    {"expr": f"neutralize(-ts_mean(rank({FIELD}), 20), subindustry)", "decay": 0}
]

alpha_list = []
for v in VARIANTS:
    s = settings.copy()
    s["decay"] = v["decay"]
    alpha_list.append({"type": "REGULAR", "settings": s, "regular": v["expr"]})

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "iter3_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} iter3 variants to {out_path}")
