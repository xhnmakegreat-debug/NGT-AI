#!/usr/bin/env python3
"""
NGT-AI 决策系统主程序 - 多API提供器版本
基于名义小组技术的多AI协作决策系统

Version: 2.1
Author: NGT-AI Team
支持的API: OpenAI, Google Gemini, DeepSeek, Qwen, xAI Grok
"""

import asyncio
import sys
import os
import yaml
from pathlib import Path
import logging
from datetime import datetime
from typing import Dict, Any, List

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

try:
    # 导入核心模块
    from src.core.orchestrator import NGTOrchestrator
    from src.providers.mock_provider import MockModelProvider
    from src.utils.presenter import ResultPresenter
    from src.utils.logger import setup_logger, NGTLogger
    
    # 尝试导入真实API提供器
    AVAILABLE_PROVIDERS = {}
    
    try:
        from src.providers.openai_provider import OpenAIProvider
        AVAILABLE_PROVIDERS['openai'] = OpenAIProvider
    except ImportError:
        pass
    
    try:
        from src.providers.google_provider import GoogleProvider
        AVAILABLE_PROVIDERS['google'] = GoogleProvider
    except ImportError:
        pass
    
    try:
        from src.providers.deepseek_provider import DeepSeekProvider
        AVAILABLE_PROVIDERS['deepseek'] = DeepSeekProvider
    except ImportError:
        pass
    
    try:
        from src.providers.qwen_provider import QwenProvider
        AVAILABLE_PROVIDERS['qwen'] = QwenProvider
        AVAILABLE_PROVIDERS['alibaba'] = QwenProvider  # 别名
    except ImportError:
        pass
    
    try:
        from src.providers.grok_provider import GrokProvider
        AVAILABLE_PROVIDERS['grok'] = GrokProvider
        AVAILABLE_PROVIDERS['xai'] = GrokProvider  # 别名
    except ImportError:
        pass
        
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    print("请确保项目结构正确且所有必需文件都已创建")
    sys.exit(1)

class NGTDecisionApp:
    """NGT-AI决策系统主应用类 - 多API支持版本"""
    
    def __init__(self, use_real_apis: bool = False, config_file: str = "config.yaml"):
        """
        初始化NGT决策应用
        
        Args:
            use_real_apis: 是否使用真实的API
            config_file: 配置文件路径
        """
        # 设置日志
        self.logger = setup_logger(
            name="ngt-ai-app",
            level="INFO", 
            log_file="logs/ngt_ai_app.log",
            console_output=True
        )
        
        self.ngt_logger = NGTLogger("ngt-ai-app")
        self.use_real_apis = use_real_apis
        self.config = self._load_config(config_file)
        
        # 显示可用的API提供器
        self.logger.info(f"可用的API提供器: {list(AVAILABLE_PROVIDERS.keys())}")
        
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
    
    def _load_config(self, config_file: str) -> dict:
        """加载配置文件"""
        try:
            config_path = Path(config_file)
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                    self.logger.info(f"已加载配置文件: {config_file}")
                    return config
            else:
                self.logger.warning(f"配置文件不存在: {config_file}，使用默认配置")
                return self._get_default_config()
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}，使用默认配置")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """获取默认配置"""
        return {
            "discussants": [
                {"ai_id": "AI_1", "model_name": "gpt-4o", "provider": "openai", "enabled": True},
                {"ai_id": "AI_2", "model_name": "gemini-1.5-pro", "provider": "google", "enabled": True},
                {"ai_id": "AI_3", "model_name": "deepseek-v2", "provider": "deepseek", "enabled": True},
                {"ai_id": "AI_4", "model_name": "qwen-long", "provider": "alibaba", "enabled": True}
            ],
            "referee": {"ai_id": "REFEREE", "model_name": "claude-3-opus", "provider": "anthropic"}
        }
    
    def _create_discussant_providers(self):
        """创建讨论员AI提供器"""
        if self.use_real_apis:
            return self._create_real_providers()
        else:
            return self._create_mock_providers()
    
    def _create_mock_providers(self):
        """创建模拟提供器"""
        providers = []
        discussant_configs = self.config.get('discussants', [])
        
        for config in discussant_configs[:4]:  # 最多4个讨论员
            if config.get('enabled', True):
                provider = MockModelProvider(
                    config['model_name'], 
                    config['ai_id']
                )
                providers.append(provider)
        
        # 如果配置的提供器不足4个，用默认的补充
        while len(providers) < 4:
            idx = len(providers) + 1
            providers.append(MockModelProvider(f"mock-model-{idx}", f"AI_{idx}"))
        
        self.logger.info(f"创建了{len(providers)}个模拟讨论员AI")
        return providers
    
    def _create_real_providers(self):
        """创建真实API提供器"""
        providers = []
        discussant_configs = self.config.get('discussants', [])
        
        for config in discussant_configs:
            if not config.get('enabled', True):
                continue
                
            provider_name = config['provider']
            ai_id = config['ai_id']
            model_name = config['model_name']
            
            # 获取API密钥
            api_key = self._get_api_key(config)
            
            if not api_key:
                self.logger.warning(f"未找到{provider_name}的API密钥，跳过{ai_id}")
                continue
            
            # 创建对应的提供器
            try:
                provider = self._create_provider(provider_name, api_key, model_name, ai_id, config)
                if provider:
                    providers.append(provider)
                    self.logger.info(f"创建{provider_name}提供器: {ai_id} ({model_name})")
            except Exception as e:
                self.logger.error(f"创建{provider_name}提供器失败: {e}")
        
        # 如果真实提供器不足，用模拟提供器补充
        while len(providers) < 4:
            idx = len(providers) + 1
            mock_provider = MockModelProvider(f"mock-model-{idx}", f"AI_{idx}")
            providers.append(mock_provider)
            self.logger.info(f"添加模拟提供器: AI_{idx}")
        
        self.logger.info(f"创建了{len(providers)}个讨论员AI提供器 (真实: {len([p for p in providers if not isinstance(p, MockModelProvider)])})")
        return providers[:4]  # 只保留前4个
    
    def _get_api_key(self, config: dict) -> str:
        """获取API密钥"""
        # 优先从配置文件获取
        api_key = config.get('api_key')
        if api_key and not api_key.startswith('${'):
            return api_key
        
        # 从环境变量获取
        provider = config['provider'].upper()
        env_keys = [
            f"{provider}_API_KEY",
            f"{config['ai_id']}_API_KEY",
            f"{config['model_name'].upper().replace('-', '_')}_API_KEY"
        ]
        
        for env_key in env_keys:
            api_key = os.getenv(env_key)
            if api_key:
                return api_key
        
        return None
    
    def _create_provider(self, provider_name: str, api_key: str, model_name: str, ai_id: str, config: dict):
        """创建指定类型的提供器"""
        provider_class = AVAILABLE_PROVIDERS.get(provider_name)
        if not provider_class:
            self.logger.warning(f"不支持的提供器: {provider_name}")
            return None
        
        try:
            # 获取base_url（如果有）
            base_url = config.get('base_url')
            
            if base_url:
                return provider_class(api_key, model_name, ai_id, base_url)
            else:
                return provider_class(api_key, model_name, ai_id)
        except Exception as e:
            self.logger.error(f"实例化{provider_name}提供器失败: {e}")
            return None
    
    def _create_referee_provider(self):
        """创建裁判AI提供器"""
        if self.use_real_apis:
            referee_config = self.config.get('referee', {})
            provider_name = referee_config.get('provider', 'anthropic')
            api_key = self._get_api_key(referee_config)
            
            if api_key and provider_name in AVAILABLE_PROVIDERS:
                try:
                    provider = self._create_provider(
                        provider_name, 
                        api_key, 
                        referee_config.get('model_name', 'claude-3-opus'),
                        referee_config.get('ai_id', 'REFEREE'),
                        referee_config
                    )
                    if provider:
                        self.logger.info(f"创建{provider_name}裁判AI提供器")
                        return provider
                except Exception as e:
                    self.logger.error(f"创建裁判AI提供器失败: {e}")
        
        # 默认使用模拟裁判
        referee = MockModelProvider("claude-3-opus", "REFEREE")
        self.logger.info("创建模拟裁判AI提供器")
        return referee
    
    def _create_dynamic_provider(self, agent_config: Dict[str, Any]):
        """
        根据前端配置动态创建AI提供器
        
        Args:
            agent_config: 智能体配置字典
            
        Returns:
            创建的提供器实例或None
        """
        try:
            agent_id = agent_config.get('id', 'UNKNOWN')
            model_name = agent_config.get('model', 'gpt-4o')
            prompt = agent_config.get('prompt', '')
            
            # 根据模型名称确定提供器类型
            provider_name = self._get_provider_name_by_model(model_name)
            
            if provider_name in AVAILABLE_PROVIDERS:
                # 尝试创建真实API提供器
                api_key = self._get_api_key_for_model(model_name)
                if api_key:
                    provider = self._create_provider(provider_name, api_key, model_name, agent_id, {})
                    if provider:
                        # 设置自定义提示词
                        provider.custom_prompt = prompt
                        self.logger.info(f"创建动态{provider_name}提供器: {agent_id}")
                        return provider
            
            # 如果无法创建真实提供器，使用模拟提供器
            mock_provider = MockModelProvider(model_name, agent_id)
            mock_provider.custom_prompt = prompt
            self.logger.info(f"创建动态模拟提供器: {agent_id} ({model_name})")
            return mock_provider
            
        except Exception as e:
            self.logger.error(f"创建动态提供器失败: {e}")
            return None
    
    def _get_provider_name_by_model(self, model_name: str) -> str:
        """根据模型名称确定提供器类型"""
        model_to_provider = {
            'gpt-4o': 'openai',
            'gpt-4': 'openai',
            'gpt-3.5-turbo': 'openai',
            'claude-3-opus': 'anthropic',
            'claude-3-sonnet': 'anthropic',
            'claude-3-haiku': 'anthropic',
            'gemini-1.5-pro': 'google',
            'gemini-1.5-flash': 'google',
            'qwen-long': 'qwen',
            'qwen-plus': 'qwen',
            'deepseek-chat': 'deepseek',
            'grok-beta': 'grok',
        }
        return model_to_provider.get(model_name, 'openai')
    
    def _get_api_key_for_model(self, model_name: str) -> str:
        """根据模型名称获取API密钥"""
        provider_name = self._get_provider_name_by_model(model_name)
        provider_upper = provider_name.upper()
        
        # 尝试从环境变量获取
        env_keys = [
            f"{provider_upper}_API_KEY",
            f"{model_name.upper().replace('-', '_')}_API_KEY"
        ]
        
        for env_key in env_keys:
            api_key = os.getenv(env_key)
            if api_key:
                return api_key
        
        return None
    
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
            return f"❌ 决策处理失败: {str(e)}\n\n💡 建议检查API配置或网络连接"
    
    async def process_decision_json_with_agents_and_progress(self, question: str, agents_config: List[Dict[str, Any]], progress_callback=None, max_retries: int = 2) -> Dict[str, Any]:
        """
        使用动态配置的AI处理决策问题并返回JSON结果，支持进度回调
        
        Args:
            question: 决策问题
            agents_config: AI智能体配置列表
            progress_callback: 进度回调函数
            max_retries: 最大重试次数
            
        Returns:
            决策结果的JSON数据
        """
        try:
            self.ngt_logger.log_stage_start("动态AI决策流程", f"问题: {question[:50]}...")
            
            # 根据配置创建动态AI提供器
            discussant_providers = []
            referee_provider = None
            
            for agent_config in agents_config:
                provider = self._create_dynamic_provider(agent_config)
                if provider:
                    if agent_config.get('type') == 'referee':
                        referee_provider = provider
                    else:
                        discussant_providers.append(provider)
            
            # 确保至少有2个讨论员和1个裁判
            if len(discussant_providers) < 2:
                self.logger.warning("讨论员数量不足，使用默认配置")
                discussant_providers = self.discussant_providers[:2]
            
            if not referee_provider:
                self.logger.warning("未配置裁判，使用默认裁判")
                referee_provider = self.referee_provider
            
            # 创建临时编排器
            from src.core.orchestrator import NGTOrchestrator
            temp_orchestrator = NGTOrchestrator(discussant_providers, referee_provider)
            
            # 执行NGT决策流程，支持进度回调
            result = await temp_orchestrator.run_decision_process_with_progress(question, max_retries, progress_callback)
            
            self.ngt_logger.log_stage_complete("动态AI决策流程", result.get('process_duration'))
            return result
            
        except Exception as e:
            self.ngt_logger.log_error("动态AI决策流程", e)
            raise
    
    async def process_decision_json_with_agents(self, question: str, agents_config: List[Dict[str, Any]], max_retries: int = 2) -> Dict[str, Any]:
        """兼容性方法，调用带进度回调的版本"""
        return await self.process_decision_json_with_agents_and_progress(question, agents_config, None, max_retries)
    
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
        real_providers = [p for p in self.discussant_providers if not isinstance(p, MockModelProvider)]
        
        return {
            "version": "2.1",
            "use_real_apis": self.use_real_apis,
            "available_providers": list(AVAILABLE_PROVIDERS.keys()),
            "discussants_count": len(self.discussant_providers),
            "real_providers_count": len(real_providers),
            "has_referee": self.referee_provider is not None,
            "discussant_models": [p.get_model_name() for p in self.discussant_providers],
            "referee_model": self.referee_provider.get_model_name() if self.referee_provider else None,
            "provider_status": {
                p.get_ai_id(): {
                    "model": p.get_model_name(),
                    "type": "real" if not isinstance(p, MockModelProvider) else "mock"
                } for p in self.discussant_providers
            }
        }
    
    def switch_api_mode(self, use_real_apis: bool):
        """切换API模式"""
        if self.use_real_apis != use_real_apis:
            self.use_real_apis = use_real_apis
            self.discussant_providers = self._create_discussant_providers()
            self.referee_provider = self._create_referee_provider()
            
            # 重新创建编排器
            self.orchestrator = NGTOrchestrator(
                self.discussant_providers,
                self.referee_provider
            )
            
            self.logger.info(f"已切换到{'真实API' if use_real_apis else '模拟'}模式")

# 其他功能函数保持不变...
def clear_screen():
    """清屏函数 - 跨平台兼容"""
    os.system('cls' if os.name == 'nt' else 'clear')

async def interactive_mode():
    """交互式模式"""
    clear_screen()
    
    print("🚀 NGT-AI 多智能体协作决策系统 v2.1")
    print("=" * 70)
    print("支持 OpenAI, Google Gemini, DeepSeek, Qwen, xAI Grok")
    print("=" * 70)
    
    # 询问使用模式
    print("\n🔧 请选择运行模式:")
    print("1. 模拟模式 (无需API密钥，快速测试)")
    print("2. 真实API模式 (需要配置API密钥)")
    
    while True:
        choice = input("\n请选择 (1-2): ").strip()
        if choice == "1":
            use_real_apis = False
            break
        elif choice == "2":
            use_real_apis = True
            break
        else:
            print("请输入 1 或 2")
    
    # 初始化系统
    try:
        app = NGTDecisionApp(use_real_apis=use_real_apis)
        print("✅ 系统初始化成功！")
    except Exception as e:
        print(f"❌ 系统初始化失败: {e}")
        return
    
    # 显示系统信息
    info = app.get_system_info()
    print(f"\n📊 系统配置:")
    print(f"   🤖 可用提供器: {', '.join(info['available_providers'])}")
    print(f"   🎯 运行模式: {'真实API' if info['use_real_apis'] else '模拟模式'}")
    print(f"   👥 讨论员: {info['discussants_count']}个 (真实: {info['real_providers_count']})")
    
    if use_real_apis:
        print(f"\n🔌 提供器状态:")
        for ai_id, status in info['provider_status'].items():
            icon = "🟢" if status['type'] == 'real' else "🔵"
            print(f"     {icon} {ai_id}: {status['model']} ({status['type']})")
    
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
        print("\n" + "=" * 70)
        print("🤔 请输入您的决策问题:")
        print("   📝 直接输入问题 | 🔢 输入1-5选择示例 | 💡 输入'help'查看帮助")
        print("   🔧 输入'switch'切换API模式 | 🔍 输入'info'查看系统信息")
        print("   🧹 输入'clear'清屏 | 👋 输入'quit'退出")
        
        user_input = input(f"\n[第{question_count + 1}次询问] 👤 您的输入: ").strip()
        
        # 处理特殊命令
        if user_input.lower() in ['quit', 'exit', '退出', 'q']:
            print(f"\n🎯 会话总结:")
            print(f"   📊 处理问题数量: {question_count}")
            print(f"   ⏱️ 会话时长: {datetime.now().strftime('%H:%M:%S')}")
            print("👋 感谢使用NGT-AI决策系统，期待下次再见！")
            break
        
        if user_input.lower() == 'clear':
            clear_screen()
            continue
        
        if user_input.lower() == 'switch':
            current_mode = "真实API" if app.use_real_apis else "模拟"
            new_mode = "模拟" if app.use_real_apis else "真实API"
            confirm = input(f"当前模式: {current_mode}，是否切换到{new_mode}模式? (y/N): ").strip().lower()
            if confirm in ['y', 'yes', '是']:
                app.switch_api_mode(not app.use_real_apis)
                print(f"✅ 已切换到{new_mode}模式")
                # 重新显示系统信息
                info = app.get_system_info()
                print(f"📊 提供器状态:")
                for ai_id, status in info['provider_status'].items():
                    icon = "🟢" if status['type'] == 'real' else "🔵"
                    print(f"     {icon} {ai_id}: {status['model']} ({status['type']})")
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
            print("\n⏱️ 预计处理时间:")
            print(f"   模拟模式: 15-30秒 | 真实API模式: 30-90秒")
            print("🔄 过程完全透明，可追溯每个决策环节")
            continue
        
        if user_input.lower() == 'info':
            info = app.get_system_info()
            print(f"\n🔧 系统详细信息:")
            print(f"   版本: {info['version']}")
            print(f"   可用提供器: {', '.join(info['available_providers'])}")
            print(f"   当前模式: {'真实API' if info['use_real_apis'] else '模拟模式'}")
            print(f"   讨论员数量: {info['discussants_count']} (真实: {info['real_providers_count']})")
            print(f"   裁判模型: {info['referee_model']}")
            print(f"\n🔌 各AI状态:")
            for ai_id, status in info['provider_status'].items():
                icon = "🟢" if status['type'] == 'real' else "🔵"
                print(f"     {icon} {ai_id}: {status['model']} ({status['type']})")
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
        print(f"\n⚙️ 即将启动NGT多AI协作决策流程...")
        
        # 显示当前配置
        info = app.get_system_info()
        if info['use_real_apis']:
            real_count = info['real_providers_count']
            mock_count = info['discussants_count'] - real_count
            print(f"   🤖 使用 {real_count} 个真实API + {mock_count} 个模拟AI")
            print(f"   ⚖️ 裁判: {info['referee_model']}")
            print(f"   ⏱️ 预计耗时: 30-90秒 (受API响应速度影响)")
        else:
            print(f"   🤖 使用 4 个模拟AI进行快速测试")
            print(f"   ⏱️ 预计耗时: 15-30秒")
        
        # 确认执行
        if question_count > 0:  # 第一次自动执行，后续需要确认
            confirm = input("\n🚀 是否开始分析? (Y/n): ").strip().lower()
            if confirm in ['n', 'no', '否']:
                print("⏹️ 已取消，您可以输入新问题")
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
                        f.write(f"API模式: {'真实API' if info['use_real_apis'] else '模拟模式'}\n")
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
            if app.use_real_apis:
                print("   1. 检查API密钥配置")
                print("   2. 检查网络连接")
                print("   3. 尝试切换到模拟模式测试")
            else:
                print("   1. 重新启动程序")
                print("   2. 检查项目文件完整性")
            continue
        
        # 继续提示
        print(f"\n" + "=" * 70)
        input("📖 按回车键继续下一个问题...")

async def single_question_mode(question: str, use_real_apis: bool = False):
    """单问题模式"""
    print(f"🚀 NGT-AI决策系统 - 单问题模式")
    print(f"📝 问题: {question}")
    print("⏳ 正在处理...")
    
    try:
        app = NGTDecisionApp(use_real_apis=use_real_apis)
        result = await app.process_decision(question)
        print("\n" + "="*80)
        print(result)
    except Exception as e:
        print(f"❌ 处理失败: {str(e)}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='NGT-AI 多智能体协作决策系统 v2.1')
    parser.add_argument('--question', '-q', type=str, help='直接处理指定问题')
    parser.add_argument('--version', '-v', action='store_true', help='显示版本信息')
    parser.add_argument('--real-api', action='store_true', help='使用真实API（需要配置密钥）')
    parser.add_argument('--config', '-c', type=str, default='config.yaml', help='指定配置文件路径')
    parser.add_argument('--list-providers', action='store_true', help='列出可用的API提供器')
    
    args = parser.parse_args()
    
    if args.version:
        print("NGT-AI Decision System v2.1")
        print("基于名义小组技术的多AI协作决策系统")
        print(f"支持的API提供器: {', '.join(AVAILABLE_PROVIDERS.keys())}")
        return
    
    if args.list_providers:
        print("🔌 可用的API提供器:")
        for provider_name in AVAILABLE_PROVIDERS.keys():
            print(f"   ✅ {provider_name}")
        print("\n💡 使用方法:")
        print("   1. 在 config.yaml 中配置对应的API密钥")
        print("   2. 或设置环境变量: {PROVIDER}_API_KEY")
        print("   3. 运行时添加 --real-api 参数")
        return
    
    try:
        if args.question:
            # 单问题模式
            asyncio.run(single_question_mode(args.question, args.real_api))
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