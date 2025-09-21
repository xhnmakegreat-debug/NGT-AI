"""
结果呈现器
负责格式化和美化NGT决策结果的输出
"""

from typing import Dict, Any, List
from datetime import datetime
import json

class ResultPresenter:
    """NGT决策结果呈现器"""
    
    @staticmethod
    def format_result(result: Dict[str, Any]) -> str:
        """
        格式化决策结果为用户友好的文本
        
        Args:
            result: NGT决策结果字典
            
        Returns:
            格式化的文本报告
        """
        output = []
        
        # 标题和基本信息
        output.append("# 🎯 NGT-AI 多智能体协作决策报告")
        output.append("=" * 60)
        output.append(f"\n**📋 决策问题**: {result['question']}")
        output.append(f"**⏱️ 处理时长**: {result['process_duration']}")
        output.append(f"**🤖 参与AI数量**: {result['participants']['total']} ({result['participants']['discussants']}个讨论员 + {result['participants']['referee']}个裁判)")
        output.append(f"**📊 完成阶段**: {result['total_stages']}/6")
        output.append(f"**📅 生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 处理统计
        stats = result['statistics']
        output.append(f"\n## 📈 决策流程统计")
        output.append(f"- **观点生成**: {stats['total_ideas']} 个初始观点")
        output.append(f"- **观点修正**: {stats['revised_count']} 个观点被修正")
        output.append(f"- **观点捍卫**: {stats['defended_count']} 个观点被捍卫")
        output.append(f"- **平均得分**: {stats['average_score']}/100")
        output.append(f"- **完成率**: {stats['completion_rate']:.1%}")
        if stats['error_count'] > 0:
            output.append(f"- **错误次数**: {stats['error_count']}")
        
        # 初始观点展示
        output.append(f"\n## 💡 初始观点生成阶段")
        output.append("各AI独立分析后的原始观点：")
        
        for i, idea in enumerate(result['initial_ideas'], 1):
            output.append(f"\n### {i}. **{idea['ai_id']}** ({idea['model_name']})")
            output.append(f"{idea['conclusion']}")
        
        # 评分阶段（如果有数据）
        if result.get('score_sheets'):
            output.append(f"\n## 🔄 交叉评分阶段")
            output.append("AI们相互评分的结果：")
            
            # 简化的评分展示
            score_summary = ResultPresenter._summarize_scores(result['score_sheets'])
            for ai_id, summary in score_summary.items():
                output.append(f"\n**{ai_id}的得分情况**:")
                output.append(f"- 平均分: {summary['avg']:.1f}/5")
                output.append(f"- 评价次数: {summary['count']}")
                if summary['highest_reason']:
                    output.append(f"- 最高评价: {summary['highest_reason']}")
        
        # 最终决策阶段
        output.append(f"\n## 🎯 最终决策阶段")
        output.append("基于同伴反馈后的最终观点：")
        
        for i, decision in enumerate(result['final_decisions'], 1):
            output.append(f"\n### {i}. **{decision['ai_id']}** - {decision['action']} ⭐{decision['final_score']:.1f}/100")
            
            if decision['action'] == 'REVISED' and decision['final_conclusion']:
                output.append(f"**🔄 修正观点**: {decision['final_conclusion']}")
            elif decision['action'] == 'DEFENDED' and decision['defense_statement']:
                output.append(f"**🛡️ 辩护声明**: {decision['defense_statement']}")
            
            # 显示原始观点对比
            output.append(f"**📝 原始观点**: {decision['initial_conclusion'][:100]}...")
        
        # 裁判分析
        if result['referee_analysis']:
            ref_analysis = result['referee_analysis']
            output.append(f"\n## ⚖️ 裁判综合分析")
            
            # 合并观点
            if ref_analysis['merged_ideas']:
                output.append(f"\n### 🔗 观点合并")
                for idea in ref_analysis['merged_ideas']:
                    sources = ', '.join(idea['source_ai_ids'])
                    output.append(f"**{idea['merged_idea_id']}** (整合自: {sources})")
                    output.append(f"{idea['content']}")
                    output.append("")
            
            # 突出观点
            if ref_analysis['highlighted_ideas']:
                output.append(f"### ✨ 亮点观点")
                for highlight in ref_analysis['highlighted_ideas']:
                    output.append(f"**来源**: {highlight['source_ai_id']}")
                    output.append(f"**内容**: {highlight['content']}")
                    output.append(f"**亮点原因**: {highlight['reason_for_highlight']}")
                    output.append("")
            
            # 风险分析
            if ref_analysis['risk_analysis_summary']:
                output.append(f"### ⚠️ 风险分析")
                for risk in ref_analysis['risk_analysis_summary']:
                    risk_emoji = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                    emoji = risk_emoji.get(risk['risk_level'], "⚪")
                    
                    output.append(f"**{risk['option_id']}** {emoji} 风险等级: {risk['risk_level']}")
                    
                    if risk['pros']:
                        output.append("**优势**:")
                        for pro in risk['pros']:
                            output.append(f"  ✅ {pro}")
                    
                    if risk['cons']:
                        output.append("**风险**:")
                        for con in risk['cons']:
                            output.append(f"  ❌ {con}")
                    output.append("")
            
            # 最终建议
            output.append(f"### 🎯 裁判最终建议")
            output.append(f"{ref_analysis['final_recommendation']}")
        
        # 决策摘要
        output.append(f"\n## 📋 决策摘要")
        output.append(ResultPresenter._generate_executive_summary(result))
        
        # 实施建议
        output.append(f"\n## 🚀 实施建议")
        output.append(ResultPresenter._generate_implementation_advice(result))
        
        # 技术信息（可选）
        if result.get('process_info'):
            output.append(f"\n---")
            output.append(f"**技术信息**: 本报告由NGT-AI系统生成，采用名义小组技术确保决策的多样性和客观性。")
        
        return "\n".join(output)
    
    @staticmethod
    def _summarize_scores(score_sheets: List[Dict]) -> Dict[str, Dict]:
        """汇总评分信息"""
        summary = {}
        
        for sheet in score_sheets:
            for ai_id, score_data in sheet['scores'].items():
                if score_data is None:  # 跳过自评
                    continue
                    
                if ai_id not in summary:
                    summary[ai_id] = {
                        'scores': [],
                        'reasons': []
                    }
                
                summary[ai_id]['scores'].append(score_data['score'])
                summary[ai_id]['reasons'].append(score_data['reason'])
        
        # 计算统计信息
        for ai_id in summary:
            scores = summary[ai_id]['scores']
            if scores:
                summary[ai_id]['avg'] = sum(scores) / len(scores)
                summary[ai_id]['count'] = len(scores)
                
                # 找最高分对应的理由
                max_score_idx = scores.index(max(scores))
                summary[ai_id]['highest_reason'] = summary[ai_id]['reasons'][max_score_idx]
            else:
                summary[ai_id]['avg'] = 0
                summary[ai_id]['count'] = 0
                summary[ai_id]['highest_reason'] = ""
        
        return summary
    
    @staticmethod
    def _generate_executive_summary(result: Dict[str, Any]) -> str:
        """生成执行摘要"""
        stats = result['statistics']
        
        summary_parts = []
        
        # 参与度分析
        if stats['completion_rate'] >= 0.8:
            summary_parts.append("✅ 决策流程完整，所有AI充分参与")
        else:
            summary_parts.append("⚠️ 部分AI未完成流程，可能影响决策全面性")
        
        # 共识度分析
        if stats['revised_count'] > stats['defended_count']:
            summary_parts.append("🔄 观点修正较多，显示AI们善于接受反馈并改进")
        elif stats['defended_count'] > stats['revised_count']:
            summary_parts.append("🛡️ 观点捍卫较多，显示AI们对初始判断较为坚持")
        else:
            summary_parts.append("⚖️ 修正与捍卫数量平衡，反映了良好的讨论动态")
        
        # 质量分析
        if stats['average_score'] >= 80:
            summary_parts.append("🌟 整体观点质量优秀，建议可信度高")
        elif stats['average_score'] >= 60:
            summary_parts.append("👍 整体观点质量良好，建议具有参考价值")
        else:
            summary_parts.append("📝 观点质量有待提升，建议谨慎采纳")
        
        return "\n".join(f"- {part}" for part in summary_parts)
    
    @staticmethod
    def _generate_implementation_advice(result: Dict[str, Any]) -> str:
        """生成实施建议"""
        advice = []
        
        # 基于裁判分析给建议
        if result.get('referee_analysis'):
            ref = result['referee_analysis']
            
            # 优先级建议
            if ref['merged_ideas']:
                advice.append("🎯 **优先实施**: 关注裁判合并的观点，这些代表了多个AI的共识")
            
            if ref['highlighted_ideas']:
                advice.append("💡 **创新探索**: 考虑突出观点中的创新要素，可作为长期发展方向")
            
            # 风险管控
            high_risk_count = len([r for r in ref.get('risk_analysis_summary', []) if r['risk_level'] == 'High'])
            if high_risk_count > 0:
                advice.append(f"⚠️ **风险管控**: 发现{high_risk_count}个高风险选项，建议制定详细的风险缓解计划")
        
        # 基于统计数据给建议
        stats = result['statistics']
        if stats['error_count'] > 0:
            advice.append("🔧 **流程优化**: 决策过程中出现错误，建议优化AI配置或网络环境")
        
        # 通用建议
        advice.extend([
            "📊 **定期评估**: 建议定期回顾决策效果，持续优化决策质量",
            "👥 **人工复核**: 重要决策建议结合人工专家意见，确保决策的最终质量",
            "📚 **文档记录**: 保存本次决策记录，为未来类似决策提供参考"
        ])
        
        return "\n".join(f"- {item}" for item in advice)
    
    @staticmethod
    def format_json_result(result: Dict[str, Any]) -> str:
        """格式化为JSON输出"""
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @staticmethod
    def format_brief_summary(result: Dict[str, Any]) -> str:
        """生成简要摘要"""
        stats = result['statistics']
        
        summary = f"""
🎯 **NGT-AI决策摘要**
━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 问题: {result['question'][:50]}...
⏱️ 耗时: {result['process_duration']}
🤖 参与: {result['participants']['total']}个AI
📊 结果: {stats['total_ideas']}个观点, 平均{stats['average_score']:.1f}分
🔄 动态: {stats['revised_count']}个修正, {stats['defended_count']}个捍卫

💡 核心建议: {'已生成裁判分析' if result.get('referee_analysis') else '流程未完成'}
        """.strip()
        
        return summary