"""
OpenAI模型提供器
需要安装openai包并配置API密钥
"""

from typing import List, Dict
from .base import ModelProvider

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class OpenAIProvider(ModelProvider):
    """OpenAI API提供器"""
    
    def __init__(self, api_key: str, model: str, ai_id: str):
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        super().__init__(ai_id)
        self.client = openai.AsyncOpenAI(api_key=api_key)
        self.model = model
    
    async def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=2000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API call failed: {str(e)}")
    
    def get_model_name(self) -> str:
        return self.model