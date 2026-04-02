"""
NGT决策系统核心编排器
负责协调整个NGT流程的执行
"""

import asyncio
import logging
from typing import List, Dict, Any, Optional
from dataclasses import asdict

from ..models.data_structures import (
    DiscussantInitialOutput,
    ScoreSheet,
    DiscussantFinalOutput,
    RefereeAnalysis
)
from ..providers.base import ModelProvider
from .parser import DataParser
from .state_tracker import StateTracker

logger = logging.getLogger(__name__)

class NGTOrchestrator:
    """NGT决策系统核心编排器"""
    
    def __init__(self, discussant_providers: List[ModelProvider], referee_provider: ModelProvider):
        """
        初始化编排器
        
        Args:
            discussant_providers: 讨论员AI提供器列表
            referee_provider: 裁判AI提供器
        """
        if len(discussant_providers) < 2:
            raise ValueError("至少需要2个讨论员AI")
        
        self.discussants = discussant_providers
        self.referee = referee_provider
        self.state = StateTracker()
        self.parser = DataParser()
        
        logger.info(f"NGT编排器初始化完成: {len(discussant_providers)}个讨论员 + 1个裁判")
    
    async def run_decision_process(self, user_question: str, max_retries: int = 2) -> Dict[str, Any]:
        """运行完整的NGT决策流程（无进度回调）"""
        return await self.run_decision_process_with_progress(user_question, max_retries, None)
    
    async def run_decision_process_with_progress(self, user_question: str, max_retries: int = 2, progress_callback=None) -> Dict[str, Any]:
        """
        运行完整的NGT决策流程，支持进度回调
        
        Args:
            user_question: 用户问题
            max_retries: 最大重试次数
            progress_callback: 进度回调函数
            
        Returns:
            完整的决策结果
        """
        logger.info(f"开始NGT决策流程: {user_question[:50]}...")
        self.state.start_process(user_question)
        
        try:
            # 阶段1: 独立观点生成
            if progress_callback:
                progress_callback("stage1", 20, "正在生成独立观点...")
            initial_outputs = await self._stage1_independent_ideas(max_retries)
            self.state.complete_stage1(initial_outputs)
            if progress_callback:
                progress_callback("stage1", 30, f"已完成独立观点生成，收集到{len(initial_outputs)}个观点")
            
            # 阶段3: 交叉评分与评审
            if progress_callback:
                progress_callback("stage3", 40, "正在进行交叉评分...")
            score_sheets = await self._stage3_cross_scoring(max_retries)
            self.state.complete_stage3(score_sheets)
            if progress_callback:
                progress_callback("stage3", 50, f"已完成交叉评分，收集到{len(score_sheets)}份评分表")
            
            # 阶段4: 分数聚合
            if progress_callback:
                progress_callback("stage4", 60, "正在聚合评分...")
            aggregated_scores = self._stage4_score_aggregation()
            self.state.complete_stage4()
            if progress_callback:
                progress_callback("stage4", 70, "已完成分数聚合")
            
            # 阶段5: 修正或捍卫
            if progress_callback:
                progress_callback("stage5", 80, "正在进行观点修正或捍卫...")
            final_outputs = await self._stage5_revision_defense(aggregated_scores, max_retries)
            self.state.complete_stage5(final_outputs)
            if progress_callback:
                progress_callback("stage5", 85, f"已完成观点修正，收集到{len(final_outputs)}个最终观点")
            
            # 阶段6: 裁判汇总
            if progress_callback:
                progress_callback("stage6", 90, "正在进行裁判汇总分析...")
            referee_analysis = await self._stage6_referee_analysis(max_retries)
            self.state.complete_stage6(referee_analysis)
            if progress_callback:
                progress_callback("stage6", 95, "已完成裁判汇总")
            
            # 生成最终结果
            if progress_callback:
                progress_callback("completed", 100, "正在生成最终报告...")
            result = self._generate_final_result()
            logger.info(f"NGT决策流程完成，耗时 {self.state.get_duration():.2f}秒")
            
            return result
            
        except Exception as e:
            logger.error(f"NGT决策流程失败: {str(e)}")
            self.state.record_error()
            raise
    
    async def _stage1_independent_ideas(self, max_retries: int) -> List[DiscussantInitialOutput]:
        """阶段1: 独立观点生成"""
        logger.info("阶段1: 生成独立观点")
        
        base_system_prompt = self._get_initial_idea_prompt()
        
        tasks = []
        for provider in self.discussants:
            # 检查是否有自定义提示词
            custom_prompt = getattr(provider, 'custom_prompt', None)
            if custom_prompt:
                system_prompt = f"{base_system_prompt}\n\n你的角色特点: {custom_prompt}"
            else:
                system_prompt = base_system_prompt
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": self.state.user_question}
            ]
            tasks.append(self._generate_initial_idea_with_retry(provider, messages, max_retries))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果
        valid_outputs = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"讨论员 {self.discussants[i].get_ai_id()} 生成观点失败: {result}")
                self.state.record_error()
            elif result:
                valid_outputs.append(result)
        
        if len(valid_outputs) < 2:
            raise Exception(f"有效观点数量不足 ({len(valid_outputs)})，无法继续决策流程")
        
        logger.info(f"阶段1完成，收集到 {len(valid_outputs)} 个观点")
        return valid_outputs
    
    async def _generate_initial_idea_with_retry(self, provider: ModelProvider, messages: List[Dict], max_retries: int) -> Optional[DiscussantInitialOutput]:
        """带重试的观点生成"""
        for attempt in range(max_retries + 1):
            try:
                response = await provider.generate_response(messages)
                parsed = self.parser.parse_initial_output(response)
                if parsed:
                    return parsed
                logger.warning(f"{provider.get_ai_id()} 第{attempt+1}次尝试解析失败")
            except Exception as e:
                logger.warning(f"{provider.get_ai_id()} 第{attempt+1}次调用失败: {e}")
            
            if attempt < max_retries:
                await asyncio.sleep(1)  # 重试前等待
        
        return None
    
    async def _stage3_cross_scoring(self, max_retries: int) -> List[ScoreSheet]:
        """阶段3: 交叉评分与评审"""
        logger.info("阶段3: 交叉评分与评审")
        
        # 准备观点摘要
        ideas_summary = self._format_ideas_for_scoring(self.state.initial_outputs)
        base_system_prompt = self._get_scoring_prompt()
        
        tasks = []
        for provider in self.discussants:
            # 检查是否有自定义提示词
            custom_prompt = getattr(provider, 'custom_prompt', None)
            if custom_prompt:
                system_prompt = f"{base_system_prompt}\n\n你的角色特点: {custom_prompt}"
            else:
                system_prompt = base_system_prompt
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"请对以下观点进行评分：\n\n{ideas_summary}"}
            ]
            tasks.append(self._generate_score_with_retry(provider, messages, max_retries))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果
        valid_scores = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"讨论员 {self.discussants[i].get_ai_id()} 评分失败: {result}")
                self.state.record_error()
            elif result:
                valid_scores.append(result)
        
        logger.info(f"阶段3完成，收集到 {len(valid_scores)} 份评分表")
        return valid_scores
    
    async def _generate_score_with_retry(self, provider: ModelProvider, messages: List[Dict], max_retries: int) -> Optional[ScoreSheet]:
        """带重试的评分生成"""
        for attempt in range(max_retries + 1):
            try:
                response = await provider.generate_response(messages)
                parsed = self.parser.parse_score_sheet(response)
                if parsed:
                    return parsed
                logger.warning(f"{provider.get_ai_id()} 评分解析失败，第{attempt+1}次尝试")
            except Exception as e:
                logger.warning(f"{provider.get_ai_id()} 评分调用失败: {e}")
            
            if attempt < max_retries:
                await asyncio.sleep(1)
        
        return None
    
    def _stage4_score_aggregation(self) -> Dict[str, Dict[str, Any]]:
        """阶段4: 分数聚合与反馈准备"""
        logger.info("阶段4: 聚合评分")
        
        aggregated_scores = {}
        
        # 为每个AI计算平均得分和收集反馈
        for initial_output in self.state.initial_outputs:
            ai_id = initial_output.ai_id
            scores = []
            feedbacks = []
            
            # 收集所有对该AI的评分
            for score_sheet in self.state.score_sheets:
                if ai_id in score_sheet.scores and score_sheet.scores[ai_id] is not None:
                    score_record = score_sheet.scores[ai_id]
                    scores.append(score_record.score)
                    feedbacks.append({
                        'scorer': score_sheet.scorer_ai_id,
                        'score': score_record.score,
                        'reason': score_record.reason
                    })
            
            # 计算统计数据
            if scores:
                avg_score = sum(scores) / len(scores)
                max_score = max(scores)
                min_score = min(scores)
                score_variance = sum((s - avg_score) ** 2 for s in scores) / len(scores)
            else:
                avg_score = max_score = min_score = score_variance = 0
            
            aggregated_scores[ai_id] = {
                'initial_output': initial_output,
                'average_score': avg_score,
                'max_score': max_score,
                'min_score': min_score,
                'score_variance': score_variance,
                'score_count': len(scores),
                'feedbacks': feedbacks
            }
        
        logger.info(f"阶段4完成，计算了 {len(aggregated_scores)} 个AI的聚合得分")
        return aggregated_scores
    
    async def _stage5_revision_defense(self, aggregated_scores: Dict[str, Dict[str, Any]], max_retries: int) -> List[DiscussantFinalOutput]:
        """阶段5: 修正或捍卫"""
        logger.info("阶段5: 修正或捍卫观点")
        
        tasks = []
        for ai_id, score_data in aggregated_scores.items():
            # 找到对应的provider
            provider = self._find_provider_by_id(ai_id)
            if not provider:
                logger.warning(f"未找到AI {ai_id} 对应的提供器")
                continue
            
            # 准备反馈信息
            feedback_text = self._format_feedback_for_revision(score_data)
            base_system_prompt = self._get_revision_prompt()
            
            # 检查是否有自定义提示词
            custom_prompt = getattr(provider, 'custom_prompt', None)
            if custom_prompt:
                system_prompt = f"{base_system_prompt}\n\n你的角色特点: {custom_prompt}"
            else:
                system_prompt = base_system_prompt
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"基于以下反馈，请修正或捍卫你的观点：\n\n{feedback_text}"}
            ]
            
            tasks.append(self._generate_final_output_with_retry(
                provider, messages, score_data['initial_output'].conclusion, max_retries
            ))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理结果并设置最终得分
        final_outputs = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"最终输出生成失败: {result}")
                self.state.record_error()
            elif result:
                # 从aggregated_scores中获取对应的分数
                ai_id = result.ai_id
                if ai_id in aggregated_scores:
                    result.final_score = aggregated_scores[ai_id]['average_score'] * 20  # 转换为百分制
                final_outputs.append(result)
        
        logger.info(f"阶段5完成，收集到 {len(final_outputs)} 个最终观点")
        return final_outputs
    
    async def _generate_final_output_with_retry(self, provider: ModelProvider, messages: List[Dict], 
                                              initial_conclusion: str, max_retries: int) -> Optional[DiscussantFinalOutput]:
        """带重试的最终输出生成"""
        for attempt in range(max_retries + 1):
            try:
                response = await provider.generate_response(messages)
                parsed = self.parser.parse_final_output(response, initial_conclusion)
                if parsed:
                    return parsed
                logger.warning(f"{provider.get_ai_id()} 最终输出解析失败")
            except Exception as e:
                logger.warning(f"{provider.get_ai_id()} 最终输出调用失败: {e}")
            
            if attempt < max_retries:
                await asyncio.sleep(1)
        
        return None
    
    async def _stage6_referee_analysis(self, max_retries: int) -> RefereeAnalysis:
        """阶段6: 裁判汇总与分析"""
        logger.info("阶段6: 裁判分析汇总")
        
        # 准备最终观点摘要
        final_summary = self._format_final_outputs_for_referee(self.state.final_outputs)
        base_system_prompt = self._get_referee_prompt()
        
        # 检查裁判是否有自定义提示词
        custom_prompt = getattr(self.referee, 'custom_prompt', None)
        if custom_prompt:
            system_prompt = f"{base_system_prompt}\n\n你的角色特点: {custom_prompt}"
        else:
            system_prompt = base_system_prompt
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"作为裁判AI，请分析以下观点并给出综合建议：\n\n{final_summary}"}
        ]
        
        for attempt in range(max_retries + 1):
            try:
                response = await self.referee.generate_response(messages)
                parsed = self.parser.parse_referee_analysis(response)
                if parsed:
                    logger.info("阶段6完成，裁判分析已生成")
                    return parsed
                logger.warning(f"裁判分析解析失败，第{attempt+1}次尝试")
            except Exception as e:
                logger.warning(f"裁判分析调用失败: {e}")
            
            if attempt < max_retries:
                await asyncio.sleep(2)  # 裁判分析较复杂，等待时间更长
        
        raise Exception("裁判分析生成失败，已达到最大重试次数")
    
    def _generate_final_result(self) -> Dict[str, Any]:
        """生成最终结果"""
        duration = self.state.get_duration()
        
        # 计算统计信息
        revised_count = len([o for o in self.state.final_outputs if o.action == "REVISED"])
        defended_count = len([o for o in self.state.final_outputs if o.action == "DEFENDED"])
        avg_score = (
            sum(o.final_score for o in self.state.final_outputs) / len(self.state.final_outputs)
            if self.state.final_outputs else 0
        )
        
        return {
            "question": self.state.user_question,
            "process_duration": f"{duration:.2f}秒",
            "total_stages": 6,
            "participants": {
                "discussants": len(self.discussants),
                "referee": 1,
                "total": len(self.discussants) + 1
            },
            "initial_ideas": [asdict(output) for output in self.state.initial_outputs],
            "score_sheets": [asdict(sheet) for sheet in self.state.score_sheets],
            "final_decisions": [asdict(output) for output in self.state.final_outputs],
            "referee_analysis": asdict(self.state.referee_analysis) if self.state.referee_analysis else None,
            "statistics": {
                "total_ideas": len(self.state.initial_outputs),
                "revised_count": revised_count,
                "defended_count": defended_count,
                "average_score": round(avg_score, 2),
                "error_count": self.state.error_count,
                "completion_rate": len(self.state.final_outputs) / len(self.state.initial_outputs) if self.state.initial_outputs else 0
            },
            "process_info": self.state.get_progress_info()
        }
    
    def _find_provider_by_id(self, ai_id: str) -> Optional[ModelProvider]:
        """根据AI ID查找提供器"""
        for provider in self.discussants:
            if provider.get_ai_id() == ai_id:
                return provider
        return None
    
    def _format_ideas_for_scoring(self, outputs: List[DiscussantInitialOutput]) -> str:
        """格式化观点用于评分"""
        formatted = []
        for output in outputs:
            formatted.append(f"**{output.ai_id} ({output.model_name})**:\n{output.conclusion}")
        return "\n\n".join(formatted)
    
    def _format_feedback_for_revision(self, score_data: Dict[str, Any]) -> str:
        """格式化反馈信息用于修正"""
        initial = score_data['initial_output']
        avg_score = score_data['average_score']
        feedbacks = score_data['feedbacks']
        
        feedback_text = f"**你的原始观点**:\n{initial.conclusion}\n\n"
        feedback_text += f"**评分统计**:\n"
        feedback_text += f"- 平均得分: {avg_score:.2f}/5\n"
        feedback_text += f"- 评分数量: {score_data['score_count']}\n"
        feedback_text += f"- 得分范围: {score_data['min_score']}-{score_data['max_score']}\n\n"
        
        feedback_text += f"**详细反馈**:\n"
        for feedback in feedbacks:
            feedback_text += f"- {feedback['scorer']} ({feedback['score']}/5): {feedback['reason']}\n"
        
        return feedback_text
    
    def _format_final_outputs_for_referee(self, outputs: List[DiscussantFinalOutput]) -> str:
        """格式化最终输出用于裁判分析"""
        formatted = []
        for output in outputs:
            content = ""
            content += f"**{output.ai_id}** - {output.action} (得分: {output.final_score:.1f}/100)\n"
            content += f"原始观点: {output.initial_conclusion}\n"
            
            if output.action == "REVISED" and output.final_conclusion:
                content += f"修正观点: {output.final_conclusion}\n"
            elif output.action == "DEFENDED" and output.defense_statement:
                content += f"辩护声明: {output.defense_statement}\n"
            
            formatted.append(content)
        
        return "\n".join(formatted)
    
    # ========== 系统提示词定义 ==========
    
    def _get_initial_idea_prompt(self) -> str:
        """获取初始观点生成的系统提示词"""
        return """你是一个专业的决策分析AI。请针对用户的问题，提供你的独立分析和建议。

请从你的专业角度深入分析问题，提出具体、可操作的建议。你的观点应该：
1. 具有独特性和创新性
2. 基于逻辑推理和实践经验  
3. 考虑可行性和实施风险
4. 提供具体的行动方案

请以JSON格式返回你的回答：
{
    "ai_id": "你的AI标识",
    "model_name": "你的模型名称", 
    "conclusion": "你的详细分析和建议（200-500字）"
}"""
    
    def _get_scoring_prompt(self) -> str:
        """获取评分系统提示词"""
        return """你需要对其他AI提出的观点进行客观、公正的评分。

评分标准（1-5分，5分最高）：
- 5分：观点非常优秀，具有高度创新性、强可行性和清晰逻辑
- 4分：观点优秀，大部分方面表现良好，有一定创新性
- 3分：观点合理，基本可行，但缺乏突出亮点
- 2分：观点一般，存在明显缺陷或可行性问题
- 1分：观点较差，逻辑混乱或不切实际

请仔细阅读所有观点，然后对除自己以外的每个观点进行评分。

请以JSON格式返回评分：
{
    "scorer_ai_id": "你的AI标识",
    "scores": {
        "AI_1": {"score": 评分, "reason": "评分理由"} 或 null（如果是自己）,
        "AI_2": {"score": 评分, "reason": "评分理由"} 或 null（如果是自己）,
        "AI_3": {"score": 评分, "reason": "评分理由"} 或 null（如果是自己）,
        "AI_4": {"score": 评分, "reason": "评分理由"} 或 null（如果是自己）
    }
}"""
    
    def _get_revision_prompt(self) -> str:
        """获取修正/捍卫系统提示词"""
        return """基于其他AI的评分和反馈，你现在有两个选择：

**REVISED（修正）**：如果你认为反馈合理，可以改进你的观点
**DEFENDED（捍卫）**：如果你认为原观点仍然正确，为它进行辩护

请认真考虑反馈内容，然后做出决定。无论选择哪种，都请提供充分的理由。

请以JSON格式回答：
{
    "ai_id": "你的AI标识",
    "action": "REVISED" 或 "DEFENDED",
    "final_conclusion": "如果选择REVISED，提供修正后的观点" 或 null,
    "defense_statement": "如果选择DEFENDED，提供辩护理由" 或 null
}"""
    
    def _get_referee_prompt(self) -> str:
        """获取裁判分析系统提示词"""
        return f"""作为裁判AI，请分析所有讨论员的最终观点，并提供综合分析。

你的任务：
1. **合并相似观点**：将内容相近的观点合并，形成更强的建议
2. **突出亮点观点**：识别特别创新或有价值的独特观点
3. **风险分析**：客观分析每个主要选项的优缺点和风险等级
4. **最终建议**：基于所有分析，提供结构化的决策建议

原始问题：{self.state.user_question}

请以JSON格式提供分析：
{{
    "merged_ideas": [
        {{
            "merged_idea_id": "M_1",
            "source_ai_ids": ["AI_1", "AI_2"],
            "content": "合并后的观点内容"
        }}
    ],
    "highlighted_ideas": [
        {{
            "source_ai_id": "AI_X",
            "content": "突出的观点",
            "reason_for_highlight": "突出的原因"
        }}
    ],
    "risk_analysis_summary": [
        {{
            "option_id": "M_1",
            "pros": ["优点1", "优点2"],
            "cons": ["风险1", "风险2"],
            "risk_level": "Low/Medium/High"
        }}
    ],
    "final_recommendation": "最终的综合建议和实施策略"
}}"""