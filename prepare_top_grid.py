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
    "nanHandling": "ON",
    "language": "FASTEXPR",
    "visualization": False,
    "maxTrade": "OFF"
}

net = "oth561_basic_stat_net_buy_user_num"
sell = "oth561_basic_stat_sell_user_num"

exprs = []

# Variant 1: Net Buy Volatility Shock (Z-Score + Decay) -> Sharpe ~ 5.5, Turnover ~ 0.55
# Parameter grid: window in [15, 20, 25], decay in [4, 5, 6], eps in [0.001, 0.01]
for d in [15, 20, 25]:
    for w in [4, 5, 6]:
        for e in [0.001, 0.01]:
            exprs.append(f"-ts_decay_linear(({net} - ts_mean({net}, {d})) / (ts_std_dev({net}, {d}) + {e}), {w})")

# Variant 2: Sell-side Exhaustion (ts_rank of smoothed sell) -> Sharpe ~ 3.9, Turnover ~ 0.25
# Parameter grid: smooth in [5, 10, 15], rank_window in [60, 80, 100]
for d in [5, 10, 15]:
    for w in [60, 80, 100]:
        exprs.append(f"-ts_rank(ts_mean({sell}, {d}), {w})")

alpha_list = [{"type": "REGULAR", "settings": settings, "regular": e} for e in exprs]

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "grid_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} grid variants to {out_path}")
