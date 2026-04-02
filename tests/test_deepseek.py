"""
DeepSeek API 测试脚本
测试DeepSeek API的连接和基本功能
"""

import asyncio
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

async def test_deepseek_basic():
    """测试DeepSeek基本连接"""
    print("🧪 DeepSeek API 基础测试")
    print("=" * 60)
    
    # 检查API密钥
    api_key = os.getenv('DEEPSEEK_API_KEY')
    if not api_key:
        print("❌ 未找到DEEPSEEK_API_KEY环境变量")
        print("\n💡 请先设置API密钥:")
        print("   set DEEPSEEK_API_KEY=你的密钥")
        return False
    
    print(f"✅ 找到API密钥: {api_key[:10]}...{api_key[-4:]}")
    
    # 导入DeepSeek Provider
    try:
        from src.providers.deepseek_provider import DeepSeekProvider
        print("✅ DeepSeek Provider导入成功")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("\n💡 请确保:")
        print("   1. src/providers/deepseek_provider.py 文件存在")
        print("   2. 已安装openai包: pip install openai")
        return False
    
    # 创建Provider实例
    try:
        provider = DeepSeekProvider(
            api_key=api_key,
            model="deepseek-chat",
            ai_id="TEST_AI"
        )
        print("✅ DeepSeek Provider实例化成功")
    except Exception as e:
        print(f"❌ 实例化失败: {e}")
        return False
    
    # 测试简单对话
    print("\n📝 测试1: 简单问答")
    try:
        messages = [
            {"role": "system", "content": "你是一个专业的AI助手。"},
            {"role": "user", "content": "请用一句话介绍你自己。"}
        ]
        
        print("   发送请求...")
        response = await provider.generate_response(messages, temperature=0.7)
        print(f"   ✅ 响应成功")
        print(f"   📄 响应内容: {response[:100]}...")
        
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 测试JSON格式输出
    print("\n📝 测试2: JSON格式输出")
    try:
        messages = [
            {"role": "system", "content": "你需要以JSON格式返回回答。"},
            {"role": "user", "content": '请分析"远程工作"的优缺点，并以JSON格式返回，包含advantages和disadvantages两个列表。'}
        ]
        
        print("   发送请求...")
        response = await provider.generate_response(messages, temperature=0.7)
        print(f"   ✅ 响应成功")
        
        # 尝试解析JSON
        import json
        try:
            # 提取JSON部分
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
            elif "{" in response and "}" in response:
                start = response.index("{")
                end = response.rindex("}") + 1
                json_str = response[start:end]
            else:
                json_str = response
            
            data = json.loads(json_str)
            print(f"   ✅ JSON解析成功")
            print(f"   📊 数据结构: {list(data.keys())}")
            
        except Exception as e:
            print(f"   ⚠️ JSON解析失败（但API调用成功）: {e}")
            print(f"   📄 原始响应: {response[:200]}...")
    
    except Exception as e:
        print(f"   ❌ 请求失败: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✅ DeepSeek API基础测试完成！")
    return True

async def test_deepseek_in_ngt():
    """测试DeepSeek在NGT系统中的集成"""
    print("\n🧪 DeepSeek NGT系统集成测试")
    print("=" * 60)
    
    # 导入NGT系统
    try:
        from ngt_ai_mvp import NGTDecisionApp
        print("✅ NGT系统导入成功")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    
    # 创建混合模式的应用（只用DeepSeek真实API，其他用模拟）
    try:
        print("\n⚙️ 初始化NGT系统（混合模式）...")
        
        # 先清除其他API密钥，确保只有DeepSeek是真实的
        os.environ.pop('OPENAI_API_KEY', None)
        os.environ.pop('GOOGLE_API_KEY', None)
        os.environ.pop('ANTHROPIC_API_KEY', None)
        
        app = NGTDecisionApp(use_real_apis=True)
        print("✅ 系统初始化成功")
        
        # 检查系统配置
        info = app.get_system_info()
        print(f"\n📊 系统配置:")
        print(f"   讨论员数量: {info['discussants_count']}")
        print(f"   真实API数量: {info['real_providers_count']}")
        
        print(f"\n🔌 提供器状态:")
        for ai_id, status in info['provider_status'].items():
            icon = "🟢" if status['type'] == 'real' else "🔵"
            print(f"   {icon} {ai_id}: {status['model']} ({status['type']})")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 运行简单决策测试
    print("\n📝 运行决策测试...")
    test_question = "作为一个创业公司，应该优先考虑产品质量还是快速迭代？请给出简要分析。"
    print(f"   问题: {test_question}")
    
    try:
        print("   ⏳ 处理中（预计15-45秒）...")
        result = await app.process_decision(test_question)
        
        print("\n✅ 决策分析完成！")
        print("\n" + "=" * 80)
        print("📄 分析结果:")
        print("=" * 80)
        print(result)
        
        # 保存测试结果
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/deepseek_test_{timestamp}.txt"
        
        Path("output").mkdir(exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"DeepSeek API 测试结果\n")
            f.write(f"测试时间: {datetime.now()}\n")
            f.write(f"测试问题: {test_question}\n")
            f.write("=" * 80 + "\n\n")
            f.write(result)
        
        print(f"\n💾 结果已保存到: {filename}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 决策处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """主测试流程"""
    print("🚀 DeepSeek API 完整测试流程")
    print("=" * 80)
    
    # 测试1: 基础API连接
    success1 = await test_deepseek_basic()
    
    if not success1:
        print("\n⚠️ 基础测试失败，跳过NGT集成测试")
        print("\n💡 常见问题:")
        print("   1. API密钥是否正确？")
        print("   2. 网络连接是否正常？")
        print("   3. DeepSeek账户是否有余额？")
        return
    
    # 询问是否继续NGT测试
    print("\n" + "=" * 80)
    choice = input("✅ 基础测试通过！是否继续NGT系统集成测试？(Y/n): ").strip().lower()
    
    if choice in ['', 'y', 'yes', '是']:
        # 测试2: NGT系统集成
        success2 = await test_deepseek_in_ngt()
        
        if success2:
            print("\n" + "=" * 80)
            print("🎉 所有测试完成！DeepSeek API工作正常")
            print("=" * 80)
            print("\n📌 下一步:")
            print("   1. 可以在config.yaml中配置多个API供应商")
            print("   2. 运行 python run.py 开始正式使用")
            print("   3. 尝试更复杂的决策问题")
        else:
            print("\n⚠️ NGT集成测试失败，但基础API工作正常")
    else:
        print("\n✅ 测试结束")

if __name__ == "__main__":
    try:
        # Windows控制台UTF-8编码
        if os.name == 'nt':
            os.system('chcp 65001 > nul 2>&1')
        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⛔ 测试被中断")
    except Exception as e:
        print(f"\n❌ 测试异常: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n按回车键退出...")