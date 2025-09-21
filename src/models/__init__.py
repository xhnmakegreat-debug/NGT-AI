"""
数据模型模块
定义NGT决策系统中使用的所有数据结构
"""

from .data_structures import (
    DiscussantInitialOutput,
    ScoreRecord,
    ScoreSheet,
    DiscussantFinalOutput,
    MergedIdea,
    HighlightedIdea,
    RiskAnalysis,
    RefereeAnalysis
)

__all__ = [
    'DiscussantInitialOutput',
    'ScoreRecord', 
    'ScoreSheet',
    'DiscussantFinalOutput',
    'MergedIdea',
    'HighlightedIdea',
    'RiskAnalysis',
    'RefereeAnalysis'
]