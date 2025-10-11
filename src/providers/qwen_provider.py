"""
Qwen模型提供器（通过 DashScope API）
需要安装 dashscope 包并配置API密钥
"""

from typing import List, Dict
from .base import ModelProvider

try:
    import dashscope
    from dashscope import Generation
    DASHSCOPE_AVAILABLE = True
except ImportError:
    DASHSCOPE_AVAILABLE = False

class QwenProvider(ModelProvider):
    """Qwen API提供器（基于 DashScope）"""
    
    def __init__(self, api_key: str, model: str, ai_id: str):
        if not DASHSCOPE_AVAILABLE:
            raise ImportError("DashScope package not installed. Run: pip install dashscope")
        
        super().__init__(ai_id)
        dashscope.api_key = api_key  # 全局设置 API key
        self.model = model
    
    async def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        """
        messages: List[Dict]，例如 [{'role': 'user', 'content': '问题'}]
        """
        try:
            # DashScope 的 Generation.call 支持 async
            response = await Generation.acall(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000
            )
            
            if response.status_code != 200:
                raise Exception(f"API error: {response.code} - {response.message}")
            
            return response.output.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"Qwen API call failed: {str(e)}")
    
    def get_model_name(self) -> str:
        return self.model
