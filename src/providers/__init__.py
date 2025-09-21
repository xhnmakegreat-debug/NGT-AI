"""
LLM提供器模块
封装各种大语言模型API的调用
"""

from .base import ModelProvider
from .mock_provider import MockModelProvider

# 如果安装了真实API依赖，可以导入
try:
    from .openai_provider import OpenAIProvider
    _OPENAI_AVAILABLE = True
except ImportError:
    _OPENAI_AVAILABLE = False

__all__ = ['ModelProvider', 'MockModelProvider']

if _OPENAI_AVAILABLE:
    __all__.append('OpenAIProvider')