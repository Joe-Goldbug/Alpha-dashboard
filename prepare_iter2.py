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
    "nanHandling": "OFF",
    "language": "FASTEXPR",
    "visualization": False,
    "maxTrade": "OFF"
}

FIELD = "oth561_basic_stat_net_buy_user_num"
SELL = "oth561_basic_stat_sell_user_num"

VARIANTS = [
    # Variant 1: Z-Score with decay
    f"-ts_decay_linear(({FIELD} - ts_mean({FIELD}, 20)) / (ts_std_dev({FIELD}, 20) + 0.01), 5)",
    f"-ts_decay_linear(({FIELD} - ts_mean({FIELD}, 30)) / (ts_std_dev({FIELD}, 30) + 0.01), 5)",
    f"-ts_decay_linear(({FIELD} - ts_mean({FIELD}, 20)) / (ts_std_dev({FIELD}, 20) + 0.01), 10)",
    
    # Variant 2: Z-Score without decay but higher window
    f"-({FIELD} - ts_mean({FIELD}, 40)) / (ts_std_dev({FIELD}, 40) + 0.01)",
    
    # Variant 3: Group Z-Score
    f"-group_zscore(ts_mean({FIELD}, 10), sector)",
    f"-group_zscore(ts_mean({FIELD}, 10), subindustry)",
    
    # Variant 4: ts_rank on sell
    f"-ts_rank(ts_mean({SELL}, 10), 60)",
    f"-ts_rank(ts_mean({SELL}, 20), 80)",
    
    # Variant 5: Normalize and scale
    f"scale(-ts_decay_linear(({FIELD} - ts_mean({FIELD}, 20)) / (ts_std_dev({FIELD}, 20) + 0.01), 5))",
    
    # Variant 6: Use winsorize to limit outliers (helps robust universe)
    f"-winsorize(ts_decay_linear(({FIELD} - ts_mean({FIELD}, 20)) / (ts_std_dev({FIELD}, 20) + 0.01), 5), std=3)"
]

alpha_list = [{"type": "REGULAR", "settings": settings, "regular": e} for e in VARIANTS]

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "iter2_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} iter2 variants to {out_path}")
