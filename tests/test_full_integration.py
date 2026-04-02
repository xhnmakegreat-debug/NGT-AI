#!/usr/bin/env python3
"""
测试完整的前后端集成
包括进度跟踪和报告生成
"""

import asyncio
import sys
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from ngt_ai_mvp import NGTDecisionApp

async def test_full_integration():
    """测试完整的前后端集成"""
    print("🧪 测试完整的前后端集成")
    print("=" * 60)
    
    # 创建应用实例
    app = NGTDecisionApp(use_real_apis=False)
    
    # 模拟前端发送的AI配置
    agents_config = [
        {
            "id": "AI-1",
            "type": "discussant", 
            "model": "gpt-4o",
            "prompt": "严谨的战略顾问，专注于可扩展性与执行路径。"
        },
        {
            "id": "AI-2", 
            "type": "discussant",
            "model": "claude-3-opus",
            "prompt": "以用户体验为核心的产品经理，关注需求洞察。"
        },
        {
            "id": "AI-3",
            "type": "discussant",
            "model": "deepseek-chat", 
            "prompt": "偏好风险控制的合规专家，审慎评估潜在失误。"
        },
        {
            "id": "AI-4",
            "type": "discussant",
            "model": "qwen-long",
            "prompt": "注重创新突破的战略官，勇于提出颠覆方案。"
        },
        {
            "id": "REF",
            "type": "referee",
            "model": "claude-3-opus",
            "prompt": "综合全局的裁判，倾向于平衡创新与稳健。"
        }
    ]
    
    # 测试问题
    question = "作为一个创业公司，应该优先考虑产品质量还是快速迭代？"
    
    print(f"📋 测试问题: {question}")
    print(f"🤖 AI配置数量: {len(agents_config)}")
    
    # 进度跟踪
    progress_updates = []
    
    def progress_callback(stage, progress, message):
        progress_updates.append({
            "stage": stage,
            "progress": progress,
            "message": message
        })
        print(f"📊 进度更新: {stage} - {progress}% - {message}")
    
    try:
        # 调用带进度回调的方法
        result = await app.process_decision_json_with_agents_and_progress(
            question, 
            agents_config, 
            progress_callback
        )
        
        print("\n✅ 完整集成测试成功!")
        print(f"📊 处理时长: {result.get('process_duration', 'N/A')}")
        print(f"👥 参与AI数量: {result.get('participants', {}).get('total', 'N/A')}")
        print(f"💡 初始观点数量: {len(result.get('initial_ideas', []))}")
        print(f"🎯 最终决策数量: {len(result.get('final_decisions', []))}")
        print(f"📈 进度更新次数: {len(progress_updates)}")
        
        # 显示进度跟踪详情
        print("\n📊 进度跟踪详情:")
        for update in progress_updates:
            print(f"  - {update['stage']}: {update['progress']}% - {update['message']}")
        
        # 显示AI配置信息
        print("\n🔧 AI配置验证:")
        for idea in result.get('initial_ideas', []):
            print(f"  - {idea.get('ai_id')}: {idea.get('model_name')}")
        
        # 显示评分信息
        if result.get('score_sheets'):
            print("\n📊 评分信息:")
            for sheet in result.get('score_sheets', []):
                print(f"  - {sheet.get('scorer_ai_id')} 的评分表")
        
        # 显示最终决策
        if result.get('final_decisions'):
            print("\n🎯 最终决策:")
            for decision in result.get('final_decisions', []):
                print(f"  - {decision.get('ai_id')}: {decision.get('action')} (得分: {decision.get('final_score', 0):.1f})")
        
        if result.get('referee_analysis'):
            print("  - 裁判分析: 已完成")
            ref_analysis = result.get('referee_analysis', {})
            if ref_analysis.get('final_recommendation'):
                print(f"  - 最终建议: {ref_analysis['final_recommendation'][:100]}...")
        
        # 保存结果到文件
        output_file = "test_integration_result.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n💾 结果已保存到: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("🚀 开始测试完整的前后端集成")
    
    success = await test_full_integration()
    
    if success:
        print("\n🎉 所有测试通过!")
    else:
        print("\n💥 测试失败，请检查配置")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

