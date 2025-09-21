
#!/usr/bin/env python3
"""
NGT-AI系统 Windows 启动脚本
"""
import asyncio
import sys
import os
from pathlib import Path
from datetime import datetime

# 确保项目根目录在Python路径中
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

def clear_screen():
    """清屏函数 - Windows兼容"""
    os.system('cls' if os.name == 'nt' else 'clear')

def check_environment():
    """检查运行环境"""
    try:
        # 检查Python版本
        if sys.version_info < (3, 8):
            print("❌ Python版本过低，需要3.8或更高版本")
            return False
        
        # 检查核心文件
        required_files = ["ngt_ai_mvp.py", "src/core/orchestrator.py"]
        for file in required_files:
            if not Path(file).exists():
                print(f"❌ 缺少必要文件: {file}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ 环境检查失败: {e}")
        return False

async def main():
    """主函数"""
    clear_screen()
    
    print("🚀 NGT-AI 多智能体协作决策系统")
    print("=" * 60)
    print("基于名义小组技术的AI集体决策平台 v2.0")
    print("=" * 60)
    
    # 环境检查
    if not check_environment():
        print("\n💡 解决建议:")
        print("1. 确保Python 3.8+已安装")
        print("2. 检查所有必要文件是否存在")
        print("3. 运行 test_imports.py 验证项目结构")
        input("\n按回车键退出...")
        return
    
    # 导入主程序
    try:
        from ngt_ai_mvp import NGTDecisionApp
        print("✅ 系统模块加载成功")
    except ImportError as e:
        print(f"❌ 模块导入失败: {e}")
        print("\n💡 解决建议:")
        print("1. 运行 test_imports.py 检查项目结构")
        print("2. 确保所有Python文件内容正确")
        input("\n按回车键退出...")
        return
    
    # 初始化系统
    try:
        app = NGTDecisionApp(use_real_apis=False)
        print("✅ NGT-AI系统初始化成功")
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        input("\n按回车键退出...")
        return
    
    # 显示系统信息
    info = app.get_system_info()
    print(f"\n📊 系统配置:")
    print(f"   🤖 AI模型: {', '.join(info['discussant_models'])}")
    print(f"   🎯 运行模式: {'真实API' if info['use_real_apis'] else '模拟模式'}")
    print(f"   👥 参与者: {info['discussants_count']}个讨论员 + 1个裁判")
    
    # 示例问题
    sample_questions = [
        "我们公司应该如何制定远程工作政策？",
        "如何提高团队工作效率和协作质量？",
        "新产品应该采用什么定价策略？", 
        "如何在工作与生活之间找到更好的平衡？",
        "创业公司在早期阶段应该优先考虑什么？"
    ]
    
    print(f"\n💡 快速开始 - 示例问题:")
    for i, q in enumerate(sample_questions, 1):
        print(f"   {i}. {q}")
    
    # 主交互循环
    question_count = 0
    while True:
        print("\n" + "=" * 60)
        print("🤔 请输入您的决策问题:")
        print("   📝 直接输入问题 | 🔢 输入1-5选择示例 | 💡 输入'help'查看帮助")
        print("   🔍 输入'info'查看系统信息 | 🧹 输入'clear'清屏 | 👋 输入'quit'退出")
        
        user_input = input(f"\n[第{question_count + 1}次询问] 👤 您的输入: ").strip()
        
        # 处理特殊命令
        if user_input.lower() in ['quit', 'exit', '退出', 'q']:
            print(f"\n🎯 会话总结:")
            print(f"   📊 处理问题数量: {question_count}")
            print(f"   ⏱️  会话时长: {datetime.now().strftime('%H:%M:%S')}")
            print("👋 感谢使用NGT-AI决策系统，期待下次再见！")
            break
        
        if user_input.lower() == 'clear':
            clear_screen()
            continue
        
        if user_input.lower() == 'help':
            print(f"\n📖 使用帮助:")
            print("🎯 NGT-AI采用6阶段决策流程:")
            print("   1️⃣ 独立观点生成 - 4个AI独立分析")
            print("   2️⃣ 观点收集分发 - 汇总所有观点") 
            print("   3️⃣ 交叉评分评审 - AI互相评分")
            print("   4️⃣ 分数聚合反馈 - 计算平均分")
            print("   5️⃣ 修正或捍卫 - 基于反馈调整")
            print("   6️⃣ 裁判汇总分析 - 综合决策建议")
            print("\n⏱️  预计处理时间: 15-45秒")
            print("🔄 过程完全透明，可追溯每个决策环节")
            continue
        
        if user_input.lower() == 'info':
            info = app.get_system_info()
            print(f"\n🔧 系统详细信息:")
            print(f"   版本: {info['version']}")
            print(f"   真实API可用: {'是' if info['real_providers_available'] else '否'}")
            print(f"   当前模式: {'真实API' if info['use_real_apis'] else '模拟模式'}")
            print(f"   讨论员模型: {info['discussant_models']}")
            print(f"   裁判模型: {info['referee_model']}")
            continue
        
        # 处理问题选择
        question = ""
        if user_input.isdigit() and 1 <= int(user_input) <= len(sample_questions):
            question = sample_questions[int(user_input) - 1]
            print(f"✅ 已选择示例问题")
        else:
            question = user_input
        
        if not question or len(question.strip()) < 5:
            print("❌ 请输入有效问题（至少5个字符）")
            continue
        
        # 显示处理信息
        print(f"\n📋 准备分析问题:")
        print(f"   {question}")
        print(f"\n⚙️  即将启动NGT多AI协作决策流程...")
        print("   🤖 4个AI将独立分析并交叉评分")
        print("   ⚖️  1个裁判AI将进行综合分析")
        print("   ⏱️  预计耗时: 15-45秒")
        
        # 确认执行
        if question_count > 0:  # 第一次自动执行，后续需要确认
            confirm = input("\n🚀 是否开始分析? (Y/n): ").strip().lower()
            if confirm in ['n', 'no', '否']:
                print("⏹️  已取消，您可以输入新问题")
                continue
        
        # 执行决策分析
        try:
            print(f"\n⏳ 正在处理中，请稍候...")
            print("   (可以按 Ctrl+C 中断)")
            
            result = await app.process_decision(question)
            question_count += 1
            
            # 显示结果
            print("\n" + "=" * 80)
            print("🎯 NGT-AI 多智能体协作决策分析完成")
            print("=" * 80)
            print(result)
            
            # 询问是否保存
            save_choice = input(f"\n💾 是否保存结果到文件? (y/N): ").strip().lower()
            if save_choice in ['y', 'yes', '是']:
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"ngt_decision_{timestamp}.txt"
                    
                    # 确保输出目录存在
                    Path("output").mkdir(exist_ok=True)
                    
                    with open(f"output/{filename}", 'w', encoding='utf-8') as f:
                        f.write("NGT-AI 多智能体协作决策报告\n")
                        f.write("=" * 50 + "\n")
                        f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"问题: {question}\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(result)
                    
                    print(f"✅ 结果已保存到: output/{filename}")
                except Exception as e:
                    print(f"❌ 保存失败: {e}")
            
        except KeyboardInterrupt:
            print("\n⛔ 用户中断了分析过程")
            continue
        except Exception as e:
            print(f"\n❌ 分析过程出现错误: {e}")
            print("\n💡 可能的解决方案:")
            print("1. 检查网络连接")
            print("2. 重新启动程序")
            print("3. 尝试更简单的问题")
            continue
        
        # 继续提示
        print(f"\n" + "=" * 60)
        input("📖 按回车键继续下一个问题...")

if __name__ == "__main__":
    try:
        # Windows控制台UTF-8编码设置
        if os.name == 'nt':
            os.system('chcp 65001 > nul 2>&1')
        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 程序已退出")
    except Exception as e:
        print(f"\n❌ 程序运行失败: {e}")
        input("按回车键退出...")
