import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from src.sessions.session_client import get_session
from src.lib.data_client import get_datafields
from src.lib.simulation.core.session_manager import UnifiedSessionManager
from src.lib.simulation_engine import simulate_single
from loguru import logger

ALPHA_TEMPLATES = [
    "-group_zscore({field}, subindustry)",
    "-ts_rank(ts_delta({field}, 5), 20)",
    "-correlation({field}, returns, 20)",
    "({field} - ts_mean({field}, 20)) / (ts_std_dev({field}, 20) + 0.001)",
    "ts_delta(ts_mean({field}, 10), 40)",
    "-signed_power(group_rank({field}, sector) - 0.5, 3)"
]

async def generate_and_simulate(region="CHN", dataset_id="other561", universe="TOP2000U", delay=1, n_jobs=3):
    logger.info(f"🚀 启动深度经济学 Alpha 挖掘引擎 (基于 {dataset_id} / {region} / {universe})")
    
    s = get_session()
    
    logger.info("📊 拉取字段列表...")
    df_fields = get_datafields(s, instrument_type="EQUITY", region=region, delay=delay, universe=universe, dataset_id=dataset_id)
    
    if df_fields.empty:
        logger.error("❌ 获取字段失败")
        return
        
    target_keywords = ['basic_stat_buy_user_num', 'basic_stat_sell_user_num', 'basic_stat_net_buy_user_num']
    valid_fields = df_fields[
        (df_fields['type'] == 'MATRIX') & 
        (df_fields['id'].str.contains('|'.join(target_keywords)))
    ]['id'].tolist()
    
    logger.info(f"✅ 提取到 {len(valid_fields)} 个核心情绪度量字段。")
    
    alpha_expressions = []
    for field in valid_fields:
        for template in ALPHA_TEMPLATES:
            expr = template.format(field=field)
            alpha_expressions.append((field, expr))
            
    logger.info(f"🧬 共生成 {len(alpha_expressions)} 个候选 Alpha。")
    
    semaphore = asyncio.Semaphore(n_jobs)
    
    session_manager = UnifiedSessionManager()
    await session_manager.initialize()
    
    try:
        tasks = []
        for i, (field, expr) in enumerate(alpha_expressions):
            tag_name = f"o561_econ_{i}"
            
            task = simulate_single(
                session_manager=session_manager,
                alpha_expression=expr,
                region_info=(region, universe),
                name=tag_name,
                neut="SUBINDUSTRY",
                decay=3,
                delay=delay,
                stone_bag=[],
                tags=[dataset_id, "Econ_Alpha", "Retail_Contrarian"],
                semaphore=semaphore,
                max_trade="OFF"
            )
            tasks.append(task)
            
        logger.info(f"🔥 并发投递 {len(tasks)} 个回测任务...")
        await asyncio.gather(*tasks)
        logger.info("🎉 深度经济学 Alpha 挖掘任务执行完毕！")
    finally:
        await session_manager.close()

if __name__ == "__main__":
    asyncio.run(generate_and_simulate(n_jobs=3))
