import json
import os

settings = {
    "instrumentType": "EQUITY",
    "region": "CHN",
    "universe": "TOP2000U",
    "delay": 1,
    "decay": 3,  # Set decay to 3 to help margin and turnover
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

VARIANTS = [
    # Group Neutralization to help robust universe sharpe
    f"-ts_mean(group_rank({FIELD}, subindustry), 20)",
    f"-ts_mean(group_rank({FIELD}, sector), 20)",
    
    # Increase window to reduce turnover and increase margin
    f"-ts_mean(rank({FIELD}), 40)",
    f"-ts_mean(rank({FIELD}), 60)",
    
    # ts_decay_linear for smoothing
    f"-ts_decay_linear(rank({FIELD}), 20)",
    f"-ts_decay_linear(rank({FIELD}), 40)",
    
    # Power transform to boost signal strength (Margin)
    f"-signed_power(ts_mean(rank({FIELD}), 20), 2)",
    
    # Switch cross-sectional rank to time-series rank (Often passes robust universe easily)
    f"-ts_rank({FIELD}, 20)",
    f"-ts_rank({FIELD}, 40)",
]

alpha_list = [{"type": "REGULAR", "settings": settings, "regular": e} for e in VARIANTS]

# Try with decay=5 on original
settings_decay5 = settings.copy()
settings_decay5["decay"] = 5
alpha_list.append({"type": "REGULAR", "settings": settings_decay5, "regular": f"-ts_mean(rank({FIELD}), 20)"})

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "opt_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} opt variants to {out_path}")
