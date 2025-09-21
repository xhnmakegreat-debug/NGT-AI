"""
模拟模型提供器
用于测试和演示，无需真实API密钥
"""

import asyncio
import json
import random
from typing import List, Dict
from .base import ModelProvider

class MockModelProvider(ModelProvider):
    """模拟的模型提供器，用于测试"""
    
    def __init__(self, model_name: str, ai_id: str):
        super().__init__(ai_id)
        self.model_name = model_name
        
    async def generate_response(self, messages: List[Dict[str, str]], temperature: float = 0.7) -> str:
        # 模拟API调用延迟
        await asyncio.sleep(random.uniform(0.5, 2.0))
        
        user_question = messages[-1]["content"]
        
        # 根据不同的任务类型生成不同的模拟响应
        if "请对以下观点进行评分" in user_question:
            return self._generate_mock_score_response()
        elif "基于以下反馈" in user_question:
            return self._generate_mock_revision_response()
        elif "作为裁判AI" in user_question:
            return self._generate_mock_referee_response()
        else:
            return self._generate_mock_initial_response(user_question)
    
    def get_model_name(self) -> str:
        return self.model_name
    
    def _generate_mock_initial_response(self, question: str) -> str:
        """生成初始观点的模拟响应"""
        responses = {
            "AI_1": f"从技术角度分析，{question[:20]}...，我认为应该优先考虑可行性和成本效益。建议采用渐进式方法，先进行小规模测试，验证核心功能的有效性。",
            "AI_2": f"关于这个问题，我更注重用户体验和市场需求。建议深入调研目标用户的实际痛点，确保我们的解决方案真正满足用户需求，而不是闭门造车。",
            "AI_3": f"从风险管理的角度来看，这个决策需要充分评估潜在风险，建立完善的风险控制机制和应急预案。同时要考虑合规性和长期可持续性。",
            "AI_4": f"我建议采用创新思维来解决这个问题，可以考虑一些颠覆性的解决方案，打破常规思维的限制。也许我们可以从完全不同的角度来思考这个挑战。"
        }
        return json.dumps({
            "ai_id": self.ai_id,
            "model_name": self.model_name,
            "conclusion": responses.get(self.ai_id, f"这是{self.ai_id}对问题的深度分析和专业建议。")
        }, ensure_ascii=False)
    
    def _generate_mock_score_response(self) -> str:
        """生成评分的模拟响应"""
        scores = {}
        ai_ids = ["AI_1", "AI_2", "AI_3", "AI_4"]
        
        for ai_id in ai_ids:
            if ai_id != self.ai_id:  # 不对自己评分
                score = random.randint(3, 5)  # 模拟分数3-5
                reasons = [
                    "该观点具有很好的可行性和创新性",
                    "分析深入，考虑周全，建议具有实用价值",
                    "逻辑清晰，实施方案可操作性强",
                    "视角独特，为决策提供了新的思路"
                ]
                scores[ai_id] = {
                    "score": score,
                    "reason": random.choice(reasons)
                }
            else:
                scores[ai_id] = None
        
        return json.dumps({
            "scorer_ai_id": self.ai_id,
            "scores": scores
        }, ensure_ascii=False)
    
    def _generate_mock_revision_response(self) -> str:
        """生成修正或捍卫的模拟响应"""
        action = random.choice(["REVISED", "DEFENDED"])
        
        if action == "REVISED":
            revisions = [
                "基于同伴的宝贵反馈，我重新审视了原有观点，增加了更多实际执行层面的考虑因素。",
                "经过深入思考，我认为原方案需要在风险控制方面进行优化，现在提出了更加稳健的版本。",
                "听取了其他AI的建议后，我意识到还需要考虑更多利益相关者的需求，因此调整了实施策略。"
            ]
            return json.dumps({
                "ai_id": self.ai_id,
                "action": "REVISED",
                "final_conclusion": random.choice(revisions),
                "defense_statement": None
            }, ensure_ascii=False)
        else:
            defenses = [
                "经过仔细考虑各方面反馈，我仍然坚持原有观点。这个方案基于充分的分析和实践经验，具有很强的可执行性。",
                "虽然收到了一些不同意见，但我认为原始建议在当前环境下是最优选择，风险可控且收益明确。",
                "我理解其他观点的合理性，但基于我的专业判断，原方案仍是解决这个问题的最佳路径。"
            ]
            return json.dumps({
                "ai_id": self.ai_id,
                "action": "DEFENDED",
                "final_conclusion": None,
                "defense_statement": random.choice(defenses)
            }, ensure_ascii=False)
    
    def _generate_mock_referee_response(self) -> str:
        """生成裁判分析的模拟响应"""
        return json.dumps({
            "merged_ideas": [
                {
                    "merged_idea_id": "M_1",
                    "source_ai_ids": ["AI_1", "AI_2"],
                    "content": "结合技术可行性评估与用户需求调研的综合解决方案：建议采用技术与市场双驱动的策略，确保方案既有技术支撑又符合市场需求。"
                },
                {
                    "merged_idea_id": "M_2",
                    "source_ai_ids": ["AI_3", "AI_4"],
                    "content": "平衡风险控制与创新突破的策略方案：在保证基本风险可控的前提下，为创新方案预留空间，采用分阶段实施的方式。"
                }
            ],
            "highlighted_ideas": [
                {
                    "source_ai_id": "AI_4",
                    "content": "颠覆性创新思维方案",
                    "reason_for_highlight": "该方案具有高度创新性和潜在的突破性价值，虽然风险较高但可能带来巨大收益。"
                }
            ],
            "risk_analysis_summary": [
                {
                    "option_id": "M_1",
                    "pros": ["技术基础扎实", "市场需求明确", "实施风险较低"],
                    "cons": ["可能缺乏差异化", "实施周期较长", "资源投入较大"],
                    "risk_level": "Medium"
                },
                {
                    "option_id": "M_2", 
                    "pros": ["创新性强", "潜在收益高", "差异化明显"],
                    "cons": ["不确定性较高", "需要更多资源", "实施难度大"],
                    "risk_level": "High"
                }
            ],
            "final_recommendation": "建议采用M_1方案作为主要实施策略，同时建立小规模试点项目验证M_2方案中的创新元素。这种组合方式既能确保基本目标的实现，又为未来的创新突破留下空间。实施过程中应建立定期评估机制，根据实际效果适时调整策略重点。"
        }, ensure_ascii=False)