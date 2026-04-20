import asyncio
import argparse
from loguru import logger
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.sessions.session_client import get_session
from src.lib.data_client import get_datafields
from src.lib.simulation.core.session_manager import SessionManager
from src.lib.simulation_engine import simulate_single

# 经济学逻辑：散户反指与情绪极值
# 结合 other561 散户虚拟盘行为数据的核心模板
ALPHA_TEMPLATES = [
    # 1. 散户买入热度反指 (Retail Buy Heat Contrarian)
    # 逻辑：散户集中买入往往是局部顶，做空高热度，做多被忽视的票
    "-group_rank(ts_mean({field}, 5), subindustry)",
    
    # 2. 情绪加速恶化 (Sentiment Acceleration Deterioration)
    # 逻辑：散户抛售情绪加速时，可能伴随错杀，寻找反转点
    "ts_delta({field}, 3)",
    
    # 3. 散户净买入占比异常 (Retail Net Buy Ratio Anomaly)
    # 需要两个字段相除，这里做单字段的波动率异常衡量
    "({field} - ts_mean({field}, 20)) / (ts_std_dev({field}, 20) + 0.001)",
    
    # 4. 散户情绪与价格背离 (Sentiment-Price Divergence)
    # 逻辑：散户在跌势中不断加仓（抄底），往往越抄越底，顺势做空
    "correlation({field}, close, 10)",
    
    # 5. 双重排序反转 (Double Rank Reversal)
    # 逻辑：时序与截面的稳健反指
    "-rank(ts_rank({field}, 10))"
]

async def generate_and_simulate(region="CHN", dataset_id="other561", universe="TOP2000U", delay=1, n_jobs=3):
    logger.info(f"🚀 启动 {dataset_id} 数据集 ({region} / {universe}) 散户情绪反指挖掘引擎...")
    
    s = get_session()
    
    logger.info("📊 拉取字段列表...")
    df_fields = get_datafields(s, instrument_type="EQUITY", region=region, delay=delay, universe=universe, dataset_id=dataset_id)
    
    if df_fields.empty:
        logger.error("❌ 获取字段失败")
        return
        
    # 我们只取基础统计的 MATRIX 字段进行快速测试
    valid_fields = df_fields[
        (df_fields['type'] == 'MATRIX') & 
        (df_fields['id'].str.contains('basic_stat'))
    ]['id'].tolist()
    
    logger.info(f"✅ 提取到 {len(valid_fields)} 个 MATRIX 基础统计字段。")
    
    alpha_expressions = []
    for field in valid_fields:
        for template in ALPHA_TEMPLATES:
            expr = template.format(field=field)
            alpha_expressions.append((field, expr))
            
    logger.info(f"🧬 共生成 {len(alpha_expressions)} 个候选情绪反指 Alpha。")
    
    semaphore = asyncio.Semaphore(n_jobs)
    
    async with SessionManager() as session_manager:
        session_manager.cookie_jar.update_cookies(s.cookies)
        session_manager.headers.update(s.headers)
        
        tasks = []
        for i, (field, expr) in enumerate(alpha_expressions):
            # 区分买入和卖出情绪的标签
            direction = "buy" if "buy" in field else ("sell" if "sell" in field else "neutral")
            tag_name = f"o561_sent_{direction}_{i}"
            
            task = simulate_single(
                session_manager=session_manager,
                alpha_expression=expr,
                region_info=(region, universe),
                name=tag_name,
                neut="SUBINDUSTRY",
                decay=3,  # 情绪因子衰减要快
                delay=delay,
                stone_bag=[],
                tags=[dataset_id, "Sentiment_Contrarian", direction],
                semaphore=semaphore,
                max_trade="OFF"
            )
            tasks.append(task)
            
        logger.info(f"🔥 并发投递 {len(tasks)} 个回测任务...")
        await asyncio.gather(*tasks)
        logger.info("🎉 散户情绪反指 Alpha 挖掘任务投递完毕！")

if __name__ == "__main__":
    asyncio.run(generate_and_simulate())
