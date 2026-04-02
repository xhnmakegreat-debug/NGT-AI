#!/usr/bin/env python3
"""
测试动态AI配置功能
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from ngt_ai_mvp import NGTDecisionApp

async def test_dynamic_agents():
    """测试动态AI配置功能"""
    print("🧪 测试动态AI配置功能")
    print("=" * 50)
    
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
    
    try:
        # 调用新的动态AI方法
        result = await app.process_decision_json_with_agents(question, agents_config)
        
        print("\n✅ 动态AI配置测试成功!")
        print(f"📊 处理时长: {result.get('process_duration', 'N/A')}")
        print(f"👥 参与AI数量: {result.get('participants', {}).get('total', 'N/A')}")
        print(f"💡 初始观点数量: {len(result.get('initial_ideas', []))}")
        print(f"🎯 最终决策数量: {len(result.get('final_decisions', []))}")
        
        # 显示AI配置信息
        print("\n🔧 AI配置验证:")
        for idea in result.get('initial_ideas', []):
            print(f"  - {idea.get('ai_id')}: {idea.get('model_name')}")
        
        if result.get('referee_analysis'):
            print("  - 裁判分析: 已完成")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主函数"""
    print("🚀 开始测试动态AI配置功能")
    
    success = await test_dynamic_agents()
    
    if success:
        print("\n🎉 所有测试通过!")
    else:
        print("\n💥 测试失败，请检查配置")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())

