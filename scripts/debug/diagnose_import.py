#!/usr/bin/env python3
"""
诊断NGT-AI系统导入问题
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

print("🔍 NGT-AI 导入诊断工具")
print("=" * 60)

# 测试1: 检查文件存在
print("\n1️⃣ 检查文件存在性...")
files_to_check = [
    "ngt_ai_mvp.py",
    "src/__init__.py",
    "src/core/__init__.py",
    "src/core/orchestrator.py",
    "src/providers/__init__.py",
    "src/providers/mock_provider.py",
]

all_exist = True
for file_path in files_to_check:
    exists = (project_root / file_path).exists()
    status = "✅" if exists else "❌"
    print(f"  {status} {file_path}")
    if not exists:
        all_exist = False

if not all_exist:
    print("\n❌ 某些必需文件不存在！")
    sys.exit(1)

# 测试2: 逐步导入测试
print("\n2️⃣ 测试模块导入...")

# 测试基础模块
try:
    from src.models.data_structures import DiscussantInitialOutput
    print("  ✅ src.models.data_structures")
except Exception as e:
    print(f"  ❌ src.models.data_structures: {e}")

try:
    from src.providers.base import ModelProvider
    print("  ✅ src.providers.base")
except Exception as e:
    print(f"  ❌ src.providers.base: {e}")

try:
    from src.providers.mock_provider import MockModelProvider
    print("  ✅ src.providers.mock_provider")
except Exception as e:
    print(f"  ❌ src.providers.mock_provider: {e}")

try:
    from src.core.orchestrator import NGTOrchestrator
    print("  ✅ src.core.orchestrator")
except Exception as e:
    print(f"  ❌ src.core.orchestrator: {e}")
    print(f"     详细错误: {type(e).__name__}: {str(e)}")

try:
    from src.utils.presenter import ResultPresenter
    print("  ✅ src.utils.presenter")
except Exception as e:
    print(f"  ❌ src.utils.presenter: {e}")

try:
    from src.utils.logger import setup_logger
    print("  ✅ src.utils.logger")
except Exception as e:
    print(f"  ❌ src.utils.logger: {e}")

# 测试3: 导入主程序
print("\n3️⃣ 测试主程序导入...")
try:
    import ngt_ai_mvp
    print("  ✅ ngt_ai_mvp 模块导入成功")
    
    # 检查是否有NGTDecisionApp类
    if hasattr(ngt_ai_mvp, 'NGTDecisionApp'):
        print("  ✅ 找到 NGTDecisionApp 类")
        
        # 尝试实例化
        try:
            app = ngt_ai_mvp.NGTDecisionApp(use_real_apis=False)
            print("  ✅ NGTDecisionApp 实例化成功")
            
            # 测试方法
            info = app.get_system_info()
            print(f"  ✅ get_system_info() 工作正常")
            print(f"     版本: {info.get('version')}")
            print(f"     讨论员: {info.get('discussants_count')}")
            
        except Exception as e:
            print(f"  ❌ NGTDecisionApp 实例化失败: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("  ❌ ngt_ai_mvp 模块中没有 NGTDecisionApp 类")
        print(f"     可用的内容: {dir(ngt_ai_mvp)}")
        
except Exception as e:
    print(f"  ❌ ngt_ai_mvp 模块导入失败: {e}")
    import traceback
    print("\n详细错误堆栈:")
    traceback.print_exc()

# 测试4: 检查依赖包
print("\n4️⃣ 检查依赖包...")
packages_to_check = [
    "asyncio",
    "yaml",
    "logging",
    "pathlib",
]

for package in packages_to_check:
    try:
        __import__(package)
        print(f"  ✅ {package}")
    except ImportError:
        print(f"  ❌ {package} 未安装")

# 测试5: 检查可选依赖
print("\n5️⃣ 检查可选API依赖...")
optional_packages = [
    ("openai", "OpenAI API"),
    ("google.generativeai", "Google Gemini"),
    ("httpx", "HTTP客户端"),
    ("pyyaml", "YAML解析"),
]

for package, name in optional_packages:
    try:
        __import__(package)
        print(f"  ✅ {name} ({package})")
    except ImportError:
        print(f"  ⚠️  {name} ({package}) 未安装 (可选)")

print("\n" + "=" * 60)
print("诊断完成！")
print("\n💡 建议:")
print("   1. 如果有 ❌ 标记，请修复对应的问题")
print("   2. 检查文件内容是否正确")
print("   3. 确保所有 __init__.py 文件存在且非空")
print("   4. 如果仍有问题，查看详细错误堆栈")