import json
import os

# PPA Constraints applied strictly:
# 1. Operators <= 8
# 2. Same Dataset Fields <= 3
# 3. No external dataset fields (like close/returns) to avoid cross-dataset limits
# 4. Neutralization: SLOW_AND_FAST (Slow + Fast factors)
# 5. Delay: 1

PPA_TEMPLATES = [
    # Concept 1: Rate of Change in Sentiment (What is changing?) -> Operator: ts_delta (1)
    "-ts_delta({field}, 3)",
    
    # Concept 2: Anomalous Volatility Shock (What is anomalous?) -> Operators: -, ts_mean, /, ts_std_dev, + (5)
    "-({field} - ts_mean({field}, 10)) / (ts_std_dev({field}, 10) + 0.001)",
    
    # Concept 3: Relative Time-Series Positioning (What is relative?) -> Operator: ts_rank (1)
    "-ts_rank({field}, 20)",
    
    # Concept 4: Acceleration of Sentiment (What is changing structurally?) -> Operators: ts_delta, ts_delta (2)
    "-ts_delta(ts_delta({field}, 3), 3)",
    
    # Concept 5: Relative Cross-Sectional Ranking (What is relative?) -> Operators: group_rank, ts_mean (2)
    "-group_rank(ts_mean({field}, 5), subindustry)",
    
    # Concept 6: Non-linear Structural Sentiment (What is essential/structural?) -> Operators: signed_power, ts_delta (2)
    "-signed_power(ts_delta({field}, 5), 2)",
    
    # Concept 7: Mean Reversion against Smoothing (What is stable vs changing?) -> Operators: -, ts_mean (2)
    "-({field} - ts_mean({field}, 10))",
    
    # Concept 8: Sentiment Momentum Persistence (What is cumulative?) -> Operators: ts_sum, ts_delta (2)
    "-ts_sum(ts_delta({field}, 1), 5)"
]

valid_fields = [
    'oth561_basic_stat_buy_user_num', 
    'oth561_basic_stat_sell_user_num', 
    'oth561_basic_stat_net_buy_user_num'
]

alpha_list = []
for field in valid_fields:
    for template in PPA_TEMPLATES:
        expr = template.format(field=field)
        
        # PPA Specific configurations
        alpha_obj = {
            "type": "REGULAR",
            "settings": {
                "instrumentType": "EQUITY",
                "region": "CHN",
                "universe": "TOP2000U",
                "delay": 1,
                "decay": 3,
                "neutralization": "SLOW_AND_FAST",  # Required by PPA: "Slow + Fast factors"
                "truncation": 0.08,
                "pasteurization": "ON",
                "unitHandling": "VERIFY",
                "nanHandling": "ON",
                "language": "FASTEXPR",
                "visualization": False,
                "maxTrade": "OFF"
            },
            "regular": expr
        }
        alpha_list.append(alpha_obj)

os.makedirs("/data/user/skills/brain-sim-alphas-batch-track/data", exist_ok=True)
out_path = "/data/user/skills/brain-sim-alphas-batch-track/data/alpha_list_ppa_final.json"

with open(out_path, "w") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Generated {len(alpha_list)} highly compliant PPA alphas to {out_path}")
