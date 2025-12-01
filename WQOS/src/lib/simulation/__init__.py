"""
统一模拟执行框架 (Unified Simulation Framework)
作者：White Peace
日期：2025年11月

提供统一的模拟执行接口，支持：
- 单模拟策略
- 多模拟策略  
- 自动策略选择
- 统一的会话管理、进度追踪、错误处理
"""

from .unified_executor import UnifiedSimulationExecutor
from .strategies.single_simulation import SingleSimulationStrategy
from .strategies.multi_simulation import MultiSimulationStrategy

__all__ = [
    'UnifiedSimulationExecutor',
    'SingleSimulationStrategy', 
    'MultiSimulationStrategy'
]
