import json
import os

# 严格遵循 PPA 规则的 Alpha 模板 (操作符 <= 8)
# 数据集字段数量 <= 3
PPA_TEMPLATES = [
    # Template 1: rank(delta) -> 2 operators, 1 field
    "-rank(ts_delta({field}, 5))",
    
    # Template 2: group_rank(mean) -> 2 operators, 1 field
    "-group_rank(ts_mean({field}, 5), subindustry)",
    
    # Template 3: correlation -> 1 operator, 1 field (close is pv1, other561 is 1)
    "-correlation({field}, close, 10)",
    
    # Template 4: z-score -> 4 operators, 1 field
    "({field} - ts_mean({field}, 10)) / (ts_std_dev({field}, 10) + 0.001)",
    
    # Template 5: ts_rank -> 1 operator, 1 field
    "-ts_rank({field}, 20)",
    
    # Template 6: signed_power -> 2 operators, 1 field
    "-signed_power(ts_delta({field}, 3), 2)"
]

valid_fields = [
    'oth561_basic_stat_buy_user_num', 
    'oth561_basic_stat_sell_user_num', 
    'oth561_basic_stat_net_buy_user_num'
]

# We will test 3 possible exact strings for Slow + Fast factors to ensure one passes.
# WQ API typically uses "SLOW_FAST" or "SLOW_FAST_FACTORS" or "SLOW_AND_FAST_FACTORS".
neut_options = ["SLOW_FAST_FACTORS", "SLOW_FAST", "SLOW_AND_FAST_FACTORS"]

alpha_list = []
for neut in neut_options:
    for field in valid_fields:
        for template in PPA_TEMPLATES:
            expr = template.format(field=field)
            
            alpha_obj = {
                "type": "REGULAR",
                "settings": {
                    "instrumentType": "EQUITY",
                    "region": "CHN",
                    "universe": "TOP2000U",
                    "delay": 1,
                    "decay": 3,
                    "neutralization": neut,
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

with open("/data/user/skills/brain-sim-alphas-batch-track/data/alpha_list_ppa.json", "w") as f:
    json.dump(alpha_list, f, indent=2)

print(f"✅ Successfully wrote {len(alpha_list)} PPA alphas to alpha_list_ppa.json")
