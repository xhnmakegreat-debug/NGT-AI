"""
NGT-AI 决策系统
基于名义小组技术的多AI协作决策系统

此模块作为包的顶层初始化，暴露常用类型与入口类，便于外部导入：

from src import NGTOrchestrator, ModelProvider

保持轻量：避免在此处进行昂贵的导入或副作用操作。
"""

__version__ = "1.0.0"
__author__ = "NGT-AI Team"
__description__ = "Multi-AI Collaborative Decision System based on Nominal Group Technique"

# 导入核心模块
from .core.orchestrator import NGTOrchestrator
from .models.data_structures import *
from .providers.base import ModelProvider

__all__ = [
    'NGTOrchestrator',
    'ModelProvider',
    'DiscussantInitialOutput',
    'ScoreSheet',
    'DiscussantFinalOutput',
    'RefereeAnalysis'
]
