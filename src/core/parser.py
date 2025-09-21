"""
数据解析器
解析和验证LLM返回的JSON数据
"""

import json
import logging
from typing import Optional
from ..models.data_structures import (
    DiscussantInitialOutput,
    ScoreSheet,
    ScoreRecord,
    DiscussantFinalOutput,
    RefereeAnalysis,
    MergedIdea,
    HighlightedIdea,
    RiskAnalysis
)

logger = logging.getLogger(__name__)

class DataParser:
    """数据解析与验证器"""
    
    @staticmethod
    def parse_initial_output(response: str) -> Optional[DiscussantInitialOutput]:
        """解析初始观点输出"""
        try:
            data = json.loads(response)
            return DiscussantInitialOutput(
                ai_id=data["ai_id"],
                model_name=data["model_name"],
                conclusion=data["conclusion"]
            )
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            logger.error(f"Failed to parse initial output: {e}")
            logger.debug(f"Raw response: {response}")
            return None
    
    @staticmethod
    def parse_score_sheet(response: str) -> Optional[ScoreSheet]:
        """解析评分表"""
        try:
            data = json.loads(response)
            scores = {}
            
            for ai_id, score_data in data["scores"].items():
                if score_data is None:
                    scores[ai_id] = None
                else:
                    scores[ai_id] = ScoreRecord(
                        score=int(score_data["score"]),
                        reason=str(score_data["reason"])
                    )
            
            return ScoreSheet(
                scorer_ai_id=data["scorer_ai_id"],
                scores=scores
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            logger.error(f"Failed to parse score sheet: {e}")
            logger.debug(f"Raw response: {response}")
            return None
    
    @staticmethod
    def parse_final_output(response: str, initial_conclusion: str) -> Optional[DiscussantFinalOutput]:
        """解析最终输出"""
        try:
            data = json.loads(response)
            action = data["action"]
            
            if action not in ["REVISED", "DEFENDED"]:
                raise ValueError(f"Invalid action: {action}")
            
            return DiscussantFinalOutput(
                ai_id=data["ai_id"],
                initial_conclusion=initial_conclusion,
                action=action,
                final_conclusion=data.get("final_conclusion"),
                defense_statement=data.get("defense_statement")
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            logger.error(f"Failed to parse final output: {e}")
            logger.debug(f"Raw response: {response}")
            return None
    
    @staticmethod
    def parse_referee_analysis(response: str) -> Optional[RefereeAnalysis]:
        """解析裁判分析"""
        try:
            data = json.loads(response)
            
            # 解析合并观点
            merged_ideas = []
            for item in data["merged_ideas"]:
                merged_ideas.append(MergedIdea(
                    merged_idea_id=item["merged_idea_id"],
                    source_ai_ids=item["source_ai_ids"],
                    content=item["content"]
                ))
            
            # 解析突出观点
            highlighted_ideas = []
            for item in data["highlighted_ideas"]:
                highlighted_ideas.append(HighlightedIdea(
                    source_ai_id=item["source_ai_id"],
                    content=item["content"],
                    reason_for_highlight=item["reason_for_highlight"]
                ))
            
            # 解析风险分析
            risk_analysis = []
            for item in data["risk_analysis_summary"]:
                risk_level = item["risk_level"]
                if risk_level not in ["Low", "Medium", "High"]:
                    raise ValueError(f"Invalid risk level: {risk_level}")
                
                risk_analysis.append(RiskAnalysis(
                    option_id=item["option_id"],
                    pros=item["pros"],
                    cons=item["cons"],
                    risk_level=risk_level
                ))
            
            return RefereeAnalysis(
                merged_ideas=merged_ideas,
                highlighted_ideas=highlighted_ideas,
                risk_analysis_summary=risk_analysis,
                final_recommendation=data["final_recommendation"]
            )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            logger.error(f"Failed to parse referee analysis: {e}")
            logger.debug(f"Raw response: {response}")
            return None
    
    @staticmethod
    def safe_parse_json(response: str) -> Optional[dict]:
        """安全解析JSON"""
        try:
            # 尝试找到JSON内容
            response = response.strip()
            if response.startswith('```json'):
                # 移除markdown代码块标记
                start = response.find('{')
                end = response.rfind('}') + 1
                if start != -1 and end > start:
                    response = response[start:end]
            
            return json.loads(response)
        except (json.JSONDecodeError, ValueError) as e:
            logger.error(f"JSON parsing failed: {e}")
            return None