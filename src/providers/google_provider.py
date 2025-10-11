"""
Google Gemini模型提供器
需要安装: pip install google-generativeai
"""

from typing import List, Dict
from .base import ModelProvider

try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False

class GoogleProvider(ModelProvider):
    """Google Gemini API提供器"""
    
    def __init__(self, api_key: str, model: str, ai_id: str):
        if not GOOGLE_AVAILABLE:
            raise ImportError("Google Generative AI package not installed. Run: pip install google-generativeai")
        
        super().__init__(ai_id)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.model_name = model
        
        # 配置生成参数
        self.generation_config = genai.types.GenerationConfig(
            temperature=0.7,
            max_output_tokens=2000,
            top_p=0.9,
        )
    
    async def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        try:
            # 更新温度设置
            self.generation_config.temperature = temperature
            
            # 将消息格式转换为Gemini格式
            prompt = self._convert_messages_to_prompt(messages)
            
            # 生成响应
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config,
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    }
                ]
            )
            
            return response.text
            
        except Exception as e:
            raise Exception(f"Google Gemini API call failed: {str(e)}")
    
    def get_model_name(self) -> str:
        return self.model_name
    
    def _convert_messages_to_prompt(self, messages: List[Dict[str, str]]) -> str:
        """将OpenAI格式的消息转换为Gemini的prompt格式"""
        prompt_parts = []
        
        for message in messages:
            role = message["role"]
            content = message["content"]
            
            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")
        
        return "\n\n".join(prompt_parts)