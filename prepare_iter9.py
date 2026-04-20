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

VARIANTS = [
    # 1. Portfolio Net
    {"expr": "-ts_mean(rank(oth561_basic_stat_buy_portfolio_num - oth561_basic_stat_sell_portfolio_num), 20)", "decay": 5},
    
    # 2. Rebalancing Net
    {"expr": "-ts_mean(rank(oth561_basic_stat_buy_rebalancing_num - oth561_basic_stat_sell_rebalancing_num), 20)", "decay": 5},
    
    # 3. Value Net
    {"expr": "-ts_mean(rank(oth561_basic_stat_buy_rebalancing_value - oth561_basic_stat_sell_rebalancing_value), 20)", "decay": 5},
    
    # 4. Value Ratio
    {"expr": "ts_mean(rank(oth561_basic_stat_sell_rebalancing_value / (oth561_basic_stat_buy_rebalancing_value + 1)), 20)", "decay": 5},
    
    # 5. Portfolio Ratio
    {"expr": "ts_mean(rank(oth561_basic_stat_sell_portfolio_num / (oth561_basic_stat_buy_portfolio_num + 1)), 20)", "decay": 5},
    
    # 6. Rebalancing Share
    {"expr": "-ts_mean(rank(oth561_basic_stat_buy_rebalancing_share - oth561_basic_stat_sell_rebalancing_share), 20)", "decay": 5},
    
    # 7. First Buy User Num
    {"expr": "-ts_mean(rank(oth561_basic_stat_first_buy_user_num), 20)", "decay": 5},
    
    # 8. User Ratio
    {"expr": "ts_mean(rank(oth561_basic_stat_sell_user_num / (oth561_basic_stat_buy_user_num + 1)), 20)", "decay": 5}
]

alpha_list = []
for v in VARIANTS:
    s = settings.copy()
    s["decay"] = v["decay"]
    alpha_list.append({"type": "REGULAR", "settings": s, "regular": v["expr"]})

out_dir = "/workspace/brain-sim-alphas-batch-track/data"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "iter9_variants.json")

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} iter9 variants to {out_path}")
