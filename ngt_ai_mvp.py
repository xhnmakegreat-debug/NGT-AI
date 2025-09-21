#!/usr/bin/env python3
"""
NGT-AI 决策系统主程序
基于名义小组技术的多AI协作决策系统

Version: 2.0
Author: NGT-AI Team
"""

import asyncio
import sys
import os
from pathlib import Path
import logging
from datetime import datetime

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

try:
    # 导入核心模块
    from src.core.orchestrator import NGTOrchestrator
    from src.providers.mock_provider import MockModelProvider
    from src.utils.presenter import ResultPresenter
    from src.utils.logger import setup_logger, NGTLogger
    
    # 尝试导入真实API提供器（可选）
    try:
        from src.providers.openai_provider import OpenAIProvider
        REAL_PROVIDERS_AVAILABLE = True
    except ImportError:
        REAL_PROVIDERS_AVAILABLE = False
        
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    print("请确保项目结构正确且所有必需文件都已创建")
    sys.exit(1)

class NGTDecisionApp:
    """NGT-AI决策系统主应用类"""
    
    def __init__(self, use_real_apis: bool = False):
        """
        初始化NGT决策应用
        
        Args:
            use_real_apis: 是否使用真实的API（需要配置密钥）
        """
        # 设置日志
        self.logger = setup_logger(
            name="ngt-ai-app",
            level="INFO", 
            log_file="logs/ngt_ai_app.log",
            console_output=True
        )
        
        self.ngt_logger = NGTLogger("ngt-ai-app")
        self.use_real_apis = use_real_apis and REAL_PROVIDERS_AVAILABLE
        
        # 初始化模型提供器
        self.discussant_providers = self._create_discussant_providers()
        self.referee_provider = self._create_referee_provider()
        
        # 初始化编排器
        self.orchestrator = NGTOrchestrator(
            self.discussant_providers,
            self.referee_provider
        )
        
        # 结果呈现器
        self.presenter = ResultPresenter()
        
        self.logger.info(f"NGT-AI系统初始化完成 (使用{'真实API' if self.use_real_apis else '模拟API'})")
    
    def _create_discussant_providers(self):
        """创建讨论员AI提供器"""
        if self.use_real_apis:
            return self._create_real_providers()
        else:
            return self._create_mock_providers()
    
    def _create_mock_providers(self):
        """创建模拟提供器"""
        providers = [
            MockModelProvider("gpt-4o", "AI_1"),
            MockModelProvider("gemini-1.5-pro", "AI_2"),
            MockModelProvider("deepseek-v2", "AI_3"), 
            MockModelProvider("qwen-long", "AI_4")
        ]
        self.logger.info(f"创建了{len(providers)}个模拟讨论员AI")
        return providers
    
    def _create_real_providers(self):
        """创建真实API提供器"""
        providers = []
        
        # 从环境变量获取API密钥
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            try:
                providers.append(OpenAIProvider(openai_key, "gpt-4", "AI_1"))
                self.logger.info("添加OpenAI提供器")
            except Exception as e:
                self.logger.warning(f"OpenAI提供器创建失败: {e}")
        
        # 如果没有足够的真实提供器，用模拟提供器补充
        while len(providers) < 4:
            idx = len(providers) + 1
            providers.append(MockModelProvider(f"mock-model-{idx}", f"AI_{idx}"))
        
        self.logger.info(f"创建了{len(providers)}个讨论员AI提供器")
        return providers
    
    def _create_referee_provider(self):
        """创建裁判AI提供器"""
        if self.use_real_apis:
            # 尝试使用真实API作为裁判
            anthropic_key = os.getenv('ANTHROPIC_API_KEY')
            if anthropic_key:
                # 这里需要实现AnthropicProvider
                pass
        
        # 默认使用模拟裁判
        referee = MockModelProvider("claude-3-opus", "REFEREE")
        self.logger.info("创建裁判AI提供器")
        return referee
    
    async def process_decision(self, question: str, max_retries: int = 2) -> str:
        """
        处理决策问题并返回格式化结果
        
        Args:
            question: 决策问题
            max_retries: 最大重试次数
            
        Returns:
            格式化的决策报告
        """
        try:
            self.ngt_logger.log_stage_start("决策流程", f"问题: {question[:50]}...")
            
            # 执行NGT决策流程
            result = await self.orchestrator.run_decision_process(question, max_retries)
            
            # 格式化结果
            formatted_result = self.presenter.format_result(result)
            
            self.ngt_logger.log_stage_complete("决策流程", result.get('process_duration'))
            return formatted_result
            
        except Exception as e:
            self.ngt_logger.log_error("决策流程", e)
            return f"❌ 决策处理失败: {str(e)}\n\n💡 建议检查网络连接或重试"
    
    async def process_decision_json(self, question: str, max_retries: int = 2) -> dict:
        """
        处理决策问题并返回JSON结果
        
        Args:
            question: 决策问题
            max_retries: 最大重试次数
            
        Returns:
            决策结果字典
        """
        try:
            result = await self.orchestrator.run_decision_process(question, max_retries)
            return result
        except Exception as e:
            self.logger.error(f"决策处理失败: {e}")
            return {
                "error": str(e),
                "question": question,
                "status": "failed"
            }
    
    def get_system_info(self) -> dict:
        """获取系统信息"""
        return {
            "version": "2.0",
            "use_real_apis": self.use_real_apis,
            "discussants_count": len(self.discussant_providers),
            "has_referee": self.referee_provider is not None,
            "real_providers_available": REAL_PROVIDERS_AVAILABLE,
            "discussant_models": [p.get_model_name() for p in self.discussant_providers],
            "referee_model": self.referee_provider.get_model_name() if self.referee_provider else None
        }

def clear_screen():
    """清屏函数 - 跨平台兼容"""
    os.system('cls' if os.name == 'nt' else 'clear')

async def interactive_mode():
    """交互式模式"""
    clear_screen()
    
    print("🚀 NGT-AI 多智能体协作决策系统")
    print("=" * 60)
    print("基于名义小组技术的AI集体决策平台")
    print("=" * 60)
    
    # 初始化系统
    try:
        app = NGTDecisionApp(use_real_apis=False)  # 默认使用模拟模式
        print("✅ 系统初始化成功！")
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        return
    
    # 显示系统信息
    info = app.get_system_info()
    print(f"\n📊 系统信息:")
    print(f"   版本: {info['version']}")
    print(f"   模式: {'真实API' if info['use_real_apis'] else '模拟模式'}")
    print(f"   讨论员: {info['discussants_count']}个")
    print(f"   模型: {', '.join(info['discussant_models'])}")
    
    # 示例问题
    sample_questions = [
        "我们公司应该如何制定远程工作政策？",
        "如何提高团队工作效率和协作质量？", 
        "新产品应该采用什么定价策略？",
        "如何在工作与生活之间找到更好的平衡？",
        "创业公司在早期阶段应该优先考虑什么？"
    ]
    
    print(f"\n💡 示例问题 (输入数字快速选择):")
    for i, q in enumerate(sample_questions, 1):
        print(f"   {i}. {q}")
    
    # 主循环
    while True:
        print("\n" + "=" * 60)
        print("🤔 请输入您的决策问题:")
        print("   • 直接输入问题文本")
        print("   • 输入数字 1-5 选择示例问题")
        print("   • 输入 'info' 查看系统信息")
        print("   • 输入 'clear' 清屏")
        print("   • 输入 'quit' 或 'exit' 退出")
        
        user_input = input("\n👤 您的输入: ").strip()
        
        # 处理特殊命令
        if user_input.lower() in ['quit', 'exit', '退出', 'q']:
            print("👋 感谢使用NGT-AI决策系统，再见！")
            break
        
        if user_input.lower() == 'clear':
            clear_screen()
            continue
        
        if user_input.lower() == 'info':
            info = app.get_system_info()
            print(f"\n📊 系统详细信息:")
            for key, value in info.items():
                print(f"   {key}: {value}")
            continue
        
        # 处理问题选择
        question = ""
        if user_input.isdigit() and 1 <= int(user_input) <= len(sample_questions):
            question = sample_questions[int(user_input) - 1]
            print(f"📝 已选择示例问题: {question}")
        else:
            question = user_input
        
        if not question:
            print("❌ 请输入有效问题")
            continue
        
        # 确认处理
        print(f"\n📋 准备分析问题: {question[:100]}{'...' if len(question) > 100 else ''}")
        print("⏳ 正在启动NGT多AI协作流程...")
        print("   (包含6个决策阶段，预计耗时 10-60秒)")
        
        confirm = input("\n是否继续? (Y/n): ").strip().lower()
        if confirm in ['n', 'no', '否']:
            print("⏹️ 已取消")
            continue
        
        # 执行决策流程
        try:
            result = await app.process_decision(question)
            
            print("\n" + "=" * 80)
            print("🎯 NGT-AI 多智能体协作决策完成")
            print("=" * 80)
            print(result)
            
            # 询问是否保存结果
            save_choice = input("\n💾 是否保存结果到文件? (y/N): ").strip().lower()
            if save_choice in ['y', 'yes', '是']:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"ngt_decision_{timestamp}.txt"
                
                # 确保输出目录存在
                Path("output").mkdir(exist_ok=True)
                
                with open(f"output/{filename}", 'w', encoding='utf-8') as f:
                    f.write(f"NGT-AI决策报告\n")
                    f.write(f"生成时间: {datetime.now()}\n")
                    f.write(f"问题: {question}\n")
                    f.write("=" * 80 + "\n\n")
                    f.write(result)
                
                print(f"✅ 结果已保存到: output/{filename}")
            
        except KeyboardInterrupt:
            print("\n⛔ 用户中断操作")
            continue
        except Exception as e:
            print(f"\n❌ 处理失败: {str(e)}")
            continue
        
        # 等待用户查看结果
        print("\n" + "=" * 60)
        input("按回车键继续...")

async def single_question_mode(question: str):
    """单问题模式"""
    print(f"🚀 NGT-AI决策系统 - 单问题模式")
    print(f"📝 问题: {question}")
    print("⏳ 正在处理...")
    
    try:
        app = NGTDecisionApp()
        result = await app.process_decision(question)
        print("\n" + "="*80)
        print(result)
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")

def main():
    """主函数"""
    import argparse
    from datetime import datetime
    
    parser = argparse.ArgumentParser(description='NGT-AI 多智能体协作决策系统')
    parser.add_argument('--question', '-q', type=str, help='直接处理指定问题')
    parser.add_argument('--version', '-v', action='store_true', help='显示版本信息')
    parser.add_argument('--real-api', action='store_true', help='使用真实API（需要配置密钥）')
    
    args = parser.parse_args()
    
    if args.version:
        print("NGT-AI Decision System v2.0")
        print("基于名义小组技术的多AI协作决策系统")
        return
    
    try:
        if args.question:
            # 单问题模式
            asyncio.run(single_question_mode(args.question))
        else:
            # 交互式模式
            asyncio.run(interactive_mode())
    except KeyboardInterrupt:
        print("\n👋 程序已退出")
    except Exception as e:
        print(f"❌ 程序运行失败: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()