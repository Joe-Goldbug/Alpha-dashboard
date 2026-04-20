import asyncio
import argparse
from loguru import logger
import sys
import os

# 确保能导入 WQOS 模块
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.sessions.session_client import get_session
from src.lib.data_client import get_datafields
from src.lib.simulation.core.session_manager import SessionManager
from src.lib.simulation_engine import simulate_single

# 定义具有经济学意义的Alpha模板
# {field} 将被替换为 other561 数据集的真实字段
ALPHA_TEMPLATES = [
    # 1. 截面动量/相对优势 (Cross-sectional Strength)
    "group_rank({field}, subindustry)",
    
    # 2. 短期均值回归 (Short-term Mean Reversion)
    "-ts_delta({field}, 3)",
    
    # 3. 中期趋势/动量 (Medium-term Trend)
    "ts_delta(ts_mean({field}, 10), 20)",
    
    # 4. 波动率调整后的信息冲击 (Volatility-Adjusted Shock)
    "({field} - ts_mean({field}, 20)) / (ts_std_dev({field}, 20) + 0.001)",
    
    # 5. 与价格趋势的背离 (Divergence with Price Trend)
    "-correlation({field}, close, 10)",
    
    # 6. 行业中性化后的异常值 (Industry Neutralized Anomaly)
    "group_neutralize({field}, subindustry)",
    
    # 7. 稳健的横截面与时序双重排序 (Robust Double Ranking)
    "rank(ts_rank({field}, 20))",
    
    # 8. 非线性变换加速信号 (Non-linear Transformation)
    "signed_power(ts_delta({field}, 5), 2)"
]

async def generate_and_simulate(region="CHN", dataset_id="other561", universe="TOP3000", delay=1, n_jobs=3):
    logger.info(f"🚀 启动 {dataset_id} 数据集 ({region}) 经济学Alpha挖掘引擎...")
    
    # 1. 获取有效会话 (依赖本地 SessionKeeper)
    s = get_session()
    
    # 2. 拉取 other561 数据集的有效字段
    logger.info(f"📊 正在拉取 {dataset_id} 数据集的字段列表...")
    df_fields = get_datafields(s, instrument_type="EQUITY", region=region, delay=delay, universe=universe, dataset_id=dataset_id)
    
    if df_fields.empty:
        logger.error(f"❌ 未能获取到 {dataset_id} 在 {region} 的字段，请检查数据集权限或 ID 是否正确。")
        return
        
    valid_fields = df_fields[df_fields['type'] == 'MATRIX']['id'].tolist()
    if not valid_fields:
        valid_fields = df_fields['id'].tolist() # Fallback
        
    logger.info(f"✅ 成功获取 {len(valid_fields)} 个有效字段。示例: {valid_fields[:5]}")
    
    # 3. 构建表达式组合
    alpha_expressions = []
    for field in valid_fields:
        for template in ALPHA_TEMPLATES:
            expr = template.format(field=field)
            alpha_expressions.append(expr)
            
    logger.info(f"🧬 基于经济学模板，共生成 {len(alpha_expressions)} 个候选 Alpha 表达式。")
    
    # 4. 提交回测任务
    semaphore = asyncio.Semaphore(n_jobs)
    
    async with SessionManager() as session_manager:
        # 同步 cookies
        session_manager.cookie_jar.update_cookies(s.cookies)
        session_manager.headers.update(s.headers)
        
        tasks = []
        for i, expr in enumerate(alpha_expressions):
            tag_name = f"other561_econ_{i}"
            task = simulate_single(
                session_manager=session_manager,
                alpha_expression=expr,
                region_info=(region, universe),
                name=tag_name,
                neut="SUBINDUSTRY",
                decay=4,
                delay=delay,
                stone_bag=[],
                tags=[dataset_id, "Econ_Alpha", region],
                semaphore=semaphore,
                max_trade="OFF"
            )
            tasks.append(task)
            
        logger.info(f"🔥 开始并发回测 {len(tasks)} 个 Alpha...")
        await asyncio.gather(*tasks)
        logger.info("🎉 所有经济学 Alpha 挖掘任务执行完毕！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--region", type=str, default="CHN")
    parser.add_argument("--dataset", type=str, default="other561")
    parser.add_argument("--jobs", type=int, default=3)
    args = parser.parse_args()
    
    asyncio.run(generate_and_simulate(region=args.region, dataset_id=args.dataset, n_jobs=args.jobs))
