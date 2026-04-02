
"""
NGT-AI系统简化启动脚本
"""
import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

async def main():
    """主函数"""
    clear_screen()
    
    print("🚀 NGT-AI 多智能体协作决策系统")
    print("=" * 60)
    
    # 尝试导入主程序
    try:
        print("📦 正在加载系统模块...")
        from ngt_ai_mvp import NGTDecisionApp
        print("✅ 模块加载成功")
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        print("\n💡 请运行 diagnose_import.py 诊断问题")
        input("按回车键退出...")
        return
    except Exception as e:
        print(f"❌ 加载异常: {e}")
        import traceback
        traceback.print_exc()
        input("按回车键退出...")
        return
    
    # 选择模式
    print("\n🔧 请选择运行模式:")
    print("1. 模拟模式 (快速测试，无需API)")
    print("2. 真实API模式 (需要配置API密钥)")
    
    while True:
        choice = input("\n请选择 (1-2): ").strip()
        if choice == "1":
            use_real_apis = False
            print("✅ 已选择模拟模式")
            break
        elif choice == "2":
            use_real_apis = True
            print("✅ 已选择真实API模式")
            break
        else:
            print("❌ 请输入 1 或 2")
    
    # 初始化系统
    try:
        print("\n⚙️  正在初始化系统...")
        app = NGTDecisionApp(use_real_apis=use_real_apis)
        print("✅ 系统初始化成功")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按回车键退出...")
        return
    
    # 显示系统信息
    try:
        info = app.get_system_info()
        print(f"\n📊 系统配置:")
        print(f"   版本: {info.get('version', 'unknown')}")
        print(f"   模式: {'真实API' if info.get('use_real_apis') else '模拟模式'}")
        print(f"   讨论员: {info.get('discussants_count', 0)} 个")
        
        if use_real_apis:
            print(f"\n🔌 提供器状态:")
            for ai_id, status in info.get('provider_status', {}).items():
                icon = "🟢" if status['type'] == 'real' else "🔵"
                print(f"     {icon} {ai_id}: {status['model']} ({status['type']})")
    except Exception as e:
        print(f"⚠️  获取系统信息失败: {e}")
    
    # 示例问题
    sample_questions = [
        "我们公司应该如何制定远程工作政策？",
        "如何提高团队工作效率？",
        "新产品应该采用什么定价策略？",
    ]
    
    print(f"\n💡 示例问题:")
    for i, q in enumerate(sample_questions, 1):
        print(f"   {i}. {q}")
    
    # 主循环
    question_count = 0
    while True:
        print("\n" + "=" * 60)
        print("请输入问题 (输入数字选择示例，'quit'退出):")
        
        user_input = input("👤 您的输入: ").strip()
        
        # 退出
        if user_input.lower() in ['quit', 'exit', 'q', '退出']:
            print(f"\n👋 已处理 {question_count} 个问题，感谢使用！")
            break
        
        # 选择示例
        question = ""
        if user_input.isdigit() and 1 <= int(user_input) <= len(sample_questions):
            question = sample_questions[int(user_input) - 1]
            print(f"✅ 已选择: {question}")
        else:
            question = user_input
        
        if not question or len(question.strip()) < 5:
            print("❌ 请输入有效问题（至少5个字符）")
            continue
        
        # 处理问题
        try:
            print(f"\n⏳ 正在分析问题，请稍候...")
            result = await app.process_decision(question)
            question_count += 1
            
            print("\n" + "=" * 80)
            print("🎯 决策分析完成")
            print("=" * 80)
            print(result)
            
            # 询问是否保存
            save = input("\n💾 是否保存结果? (y/N): ").strip().lower()
            if save in ['y', 'yes', '是']:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"output/ngt_decision_{timestamp}.txt"
                
                Path("output").mkdir(exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(result)
                
                print(f"✅ 已保存到: {filename}")
            
        except KeyboardInterrupt:
            print("\n⛔ 用户中断")
            continue
        except Exception as e:
            print(f"\n❌ 处理失败: {e}")
            continue
        
        input("\n按回车继续...")

if __name__ == "__main__":
    try:
        # Windows控制台UTF-8编码
        if os.name == 'nt':
            os.system('chcp 65001 > nul 2>&1')
        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出")
    except Exception as e:
        print(f"\n❌ 程序错误: {e}")
        input("按回车键退出...")
