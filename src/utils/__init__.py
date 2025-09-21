"""
工具函数模块
包含日志、结果呈现等辅助功能
"""

from .logger import setup_logger, get_logger
from .presenter import ResultPresenter

__all__ = ['setup_logger', 'get_logger', 'ResultPresenter']