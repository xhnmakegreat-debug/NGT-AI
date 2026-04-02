"""
xAI Grok模型提供器
Grok使用OpenAI兼容的API接口
"""

from typing import List, Dict
from .base import ModelProvider

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class GrokProvider(ModelProvider):
    """xAI Grok API提供器 (使用OpenAI兼容接口)"""
    
    def __init__(self, api_key: str, model: str, ai_id: str, base_url: str = "https://api.x.ai/v1"):
        """
        初始化Grok提供器
        
        Args:
            api_key: API密钥
            model: 模型名称
            ai_id: AI标识符
            base_url: API端点URL（默认为xAI官方地址）
        """
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        super().__init__(ai_id)
        self.client = openai.AsyncOpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model_name = model
    
    async def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        try:
            # Grok支持的消息格式与OpenAI相同
            response = await self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=2000,
                top_p=0.9,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Grok API call failed: {str(e)}")
    
    def get_model_name(self) -> str:
        return self.model_name