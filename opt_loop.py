import os
import json
import subprocess

# The user mentioned: "Robust universe Sharpe of 0.5 is below cutoff of 0.97 (40% of Alpha)"
# This usually happens when an alpha's performance relies too heavily on one specific subuniverse
# (e.g. only working on illiquid stocks).
# To fix "Robust universe Sharpe" (Sub-universe Test), we need to DECOUPLE or WINSORIZE or
# use a decay to smooth out the extremes, OR neutralize.

# I don't have the original formula, but we are working in the context of the previous `other561` dataset.
# Let's create a base that simulates this context, but we will add the required subuniverse-robust operations.

# Typical approaches to improve Robust Universe Sharpe:
# 1. group_neutralize(x, subindustry) to remove sector bias
# 2. winsorize(x, std=3) to remove outlier biases
# 3. rank() to make it uniform across all stocks

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

# Generate 8 variants explicitly targeting "Subuniverse Robustness"
base_expr = "-ts_decay_linear((oth561_basic_stat_net_buy_user_num - ts_mean(oth561_basic_stat_net_buy_user_num, 20)) / (ts_std_dev(oth561_basic_stat_net_buy_user_num, 20) + 0.01), 5)"

exprs = [
    # 1. Rank the base to enforce uniform distribution across the universe
    f"rank({base_expr})",
    
    # 2. Winsorize to cut off extreme outliers that dominate the universe
    f"winsorize({base_expr}, std=3)",
    
    # 3. Scale to limit margin impact from a few stocks
    f"scale({base_expr})",
    
    # 4. Group rank by subindustry
    f"group_rank({base_expr}, subindustry)",
    
    # 5. Double rank to smooth out everything
    f"rank(ts_rank(oth561_basic_stat_sell_user_num, 20))",
    
    # 6. Smooth the net buy even more before using
    "-ts_rank(ts_decay_linear(oth561_basic_stat_net_buy_user_num, 10), 20)",
    
    # 7. Z-score across the cross section
    f"zscore({base_expr})",
    
    # 8. Use sign*power to dampen extremes
    f"sign({base_expr}) * power(abs({base_expr}), 0.5)"
]

alpha_list = [{"type": "REGULAR", "settings": settings, "regular": e} for e in exprs]

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "opt_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"Generated {len(alpha_list)} optimization variants for Sub-Universe Check.")
