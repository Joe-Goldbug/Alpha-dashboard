import sys
import os
import json

# 确保能导入 WQOS 模块
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.sessions.session_client import get_session
from src.lib.data_client import get_datasets, get_datafields

def explore_dataset():
    print("正在获取 Session...")
    s = get_session()
    
    print("\n--- 获取 other561 数据集信息 ---")
    datasets = get_datasets(s, instrument_type="EQUITY", region="CHN", delay=1, universe="TOP3000")
    if not datasets.empty:
        other561 = datasets[datasets['id'] == 'other561']
        if not other561.empty:
            print(json.dumps(other561.to_dict('records')[0], indent=2, ensure_ascii=False))
        else:
            print("未在 CHN 区域找到 other561 数据集的基本信息，但仍尝试获取字段。")
    
    print("\n--- 获取 other561 字段信息 ---")
    fields_df = get_datafields(s, instrument_type="EQUITY", region="CHN", delay=1, universe="TOP3000", dataset_id="other561")
    
    if fields_df.empty:
        print("未获取到字段信息。请检查是否有权限或该数据集是否在 CHN 区域可用。")
    else:
        print(f"成功获取 {len(fields_df)} 个字段。")
        print("\n字段类型分布:")
        print(fields_df['type'].value_counts().to_string())
        
        print("\n前 10 个字段示例:")
        for idx, row in fields_df.head(10).iterrows():
            desc = row.get('description', 'No description')
            print(f"- {row['id']} ({row['type']}): {desc}")
            
        # 保存到本地文件以便后续分析
        fields_df.to_csv('other561_fields.csv', index=False)
        print("\n所有字段信息已保存到 other561_fields.csv")

if __name__ == "__main__":
    explore_dataset()
