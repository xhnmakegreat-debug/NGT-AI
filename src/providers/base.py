"""
模型提供器基类
定义所有LLM提供器的通用接口
"""

from abc import ABC, abstractmethod
from typing import List, Dict

class ModelProvider(ABC):
    """LLM提供器抽象基类"""
    
    def __init__(self, ai_id: str):
        self.ai_id = ai_id
    
    @abstractmethod
    async def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        生成响应
        
        Args:
            messages: 对话消息列表
            temperature: 生成温度
            
        Returns:
            生成的响应文本
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """获取模型名称"""
        pass
    
    def get_ai_id(self) -> str:
        """获取AI标识"""
        return self.ai_id