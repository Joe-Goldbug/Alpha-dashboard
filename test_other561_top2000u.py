import sys
import os
import json
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.sessions.session_client import get_session
from src.lib.data_client import get_datasets, get_datafields

s = get_session()
print("尝试获取 other561 数据集 (CHN, TOP2000U)...")
datasets = get_datasets(s, instrument_type="EQUITY", region="CHN", delay=1, universe="TOP2000U")
if not datasets.empty:
    other561 = datasets[datasets['id'] == 'other561']
    if not other561.empty:
        print("✅ 找到数据集基本信息:")
        print(json.dumps(other561.to_dict('records')[0], indent=2, ensure_ascii=False))
    else:
        print("❌ get_datasets 接口未返回 other561")
else:
    print("❌ get_datasets 接口返回空")

print("\n尝试直接拉取 other561 字段列表...")
fields_df = get_datafields(s, instrument_type="EQUITY", region="CHN", delay=1, universe="TOP2000U", dataset_id="other561")

if not fields_df.empty:
    print(f"✅ 成功获取 {len(fields_df)} 个字段！")
    print("\n字段类型分布:")
    print(fields_df['type'].value_counts().to_string())
    
    print("\n前 20 个字段示例:")
    for idx, row in fields_df.head(20).iterrows():
        desc = row.get('description', 'No description')
        print(f"- {row['id']} ({row['type']}): {desc}")
        
    fields_df.to_csv('other561_fields_top2000u.csv', index=False)
else:
    print("❌ get_datafields 接口返回空")
