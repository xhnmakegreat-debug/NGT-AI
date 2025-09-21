"""
状态追踪器
管理NGT决策流程的状态数据
"""

import time
from typing import List, Optional
from ..models.data_structures import (
    DiscussantInitialOutput,
    ScoreSheet, 
    DiscussantFinalOutput,
    RefereeAnalysis
)

class StateTracker:
    """NGT决策流程状态追踪器"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """重置状态"""
        self.user_question: str = ""
        self.initial_outputs: List[DiscussantInitialOutput] = []
        self.score_sheets: List[ScoreSheet] = []
        self.final_outputs: List[DiscussantFinalOutput] = []
        self.referee_analysis: Optional[RefereeAnalysis] = None
        self.start_time: float = 0
        self.end_time: float = 0
        self.current_stage: str = "未开始"
        self.error_count: int = 0
        
    def start_process(self, question: str):
        """开始决策流程"""
        self.reset()
        self.user_question = question
        self.start_time = time.time()
        self.current_stage = "阶段1-独立观点生成"
    
    def complete_stage1(self, outputs: List[DiscussantInitialOutput]):
        """完成阶段1"""
        self.initial_outputs = outputs
        self.current_stage = "阶段3-交叉评分"
    
    def complete_stage3(self, score_sheets: List[ScoreSheet]):
        """完成阶段3"""
        self.score_sheets = score_sheets
        self.current_stage = "阶段4-分数聚合"
    
    def complete_stage4(self):
        """完成阶段4"""
        self.current_stage = "阶段5-修正或捍卫"
    
    def complete_stage5(self, final_outputs: List[DiscussantFinalOutput]):
        """完成阶段5"""
        self.final_outputs = final_outputs
        self.current_stage = "阶段6-裁判汇总"
    
    def complete_stage6(self, referee_analysis: RefereeAnalysis):
        """完成阶段6"""
        self.referee_analysis = referee_analysis
        self.current_stage = "已完成"
        self.end_time = time.time()
    
    def get_duration(self) -> float:
        """获取处理时长"""
        if self.end_time > 0:
            return self.end_time - self.start_time
        else:
            return time.time() - self.start_time if self.start_time > 0 else 0
    
    def record_error(self):
        """记录错误"""
        self.error_count += 1
    
    def get_progress_info(self) -> dict:
        """获取进度信息"""
        return {
            "current_stage": self.current_stage,
            "duration": self.get_duration(),
            "initial_ideas_count": len(self.initial_outputs),
            "score_sheets_count": len(self.score_sheets),
            "final_outputs_count": len(self.final_outputs),
            "has_referee_analysis": self.referee_analysis is not None,
            "error_count": self.error_count
        }