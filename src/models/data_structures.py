"""
NGT-AI系统数据结构定义
"""

from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class DiscussantInitialOutput:
    """讨论员初始输出数据结构"""
    ai_id: str
    model_name: str
    conclusion: str

@dataclass
class ScoreRecord:
    """评分记录数据结构"""
    score: int  # 1-5 Likert scale
    reason: str

@dataclass
class ScoreSheet:
    """评分表数据结构"""
    scorer_ai_id: str
    scores: Dict[str, Optional[ScoreRecord]]

@dataclass
class DiscussantFinalOutput:
    """讨论员最终输出数据结构"""
    ai_id: str
    initial_conclusion: str
    action: str  # "REVISED" or "DEFENDED"
    final_conclusion: Optional[str] = None
    defense_statement: Optional[str] = None
    final_score: float = 0.0

@dataclass
class MergedIdea:
    """合并观点数据结构"""
    merged_idea_id: str
    source_ai_ids: List[str]
    content: str

@dataclass
class HighlightedIdea:
    """突出观点数据结构"""
    source_ai_id: str
    content: str
    reason_for_highlight: str

@dataclass
class RiskAnalysis:
    """风险分析数据结构"""
    option_id: str
    pros: List[str]
    cons: List[str]
    risk_level: str  # "Low", "Medium", "High"

@dataclass
class RefereeAnalysis:
    """裁判分析数据结构"""
    merged_ideas: List[MergedIdea]
    highlighted_ideas: List[HighlightedIdea]
    risk_analysis_summary: List[RiskAnalysis]
    final_recommendation: str