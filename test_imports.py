#!/usr/bin/env python3
"""
NGT-AI 项目结构和导入测试
用于验证项目文件完整性和模块导入正确性
"""

import sys
import os
from pathlib import Path
import argparse

def test_project_structure():
    """测试项目结构完整性"""
    print("🔍 检查项目文件结构...")
    
    required_files = [
        # 根目录文件
        "ngt_ai_mvp.py",
        "run.py", 
        "config.yaml",
        "README.md",
        
        # src目录结构
        "src/__init__.py",
        
        # models模块
        "src/models/__init__.py", 
        "src/models/data_structures.py",
        
        # providers模块
        "src/providers/__init__.py",
        "src/providers/base.py",
        "src/providers/mock_provider.py",
        "src/providers/openai_provider.py",
        
        # core模块
        "src/core/__init__.py",
        "src/core/orchestrator.py",
        "src/core/parser.py",
        "src/core/state_tracker.py",
        
        # utils模块
        "src/utils/__init__.py",
        "src/utils/logger.py",
        "src/utils/presenter.py",
        
        # tests目录
        "tests/__init__.py",
        "tests/test_ngt.py",
        
        # examples目录
        "examples/sample_questions.py"
    ]
    
    # 可选文件
    optional_files = [
        "requirements-minimal.txt",
        "requirements-dev.txt", 
        "start.bat",
        "simple_install.bat",
        "quick_test.bat",
        ".gitignore",
        "LICENSE"
    ]
    
    missing_required = []
    existing_required = []
    missing_optional = []
    existing_optional = []
    
    print("\n📋 必需文件检查:")
    for file_path in required_files:
        if Path(file_path).exists():
            existing_required.append(file_path)
            print(f"  ✅ {file_path}")
        else:
            missing_required.append(file_path)
            print(f"  ❌ {file_path}")
    
    print(f"\n📋 可选文件检查:")
    for file_path in optional_files:
        if Path(file_path).exists():
            existing_optional.append(file_path)
            print(f"  ✅ {file_path}")
        else:
            missing_optional.append(file_path)
            print(f"  ➖ {file_path}")
    
    # 检查目录
    required_dirs = ["src", "src/models", "src/providers", "src/core", "src/utils", "tests", "examples"]
    optional_dirs = ["logs", "output", "data", "backups"]
    
    print(f"\n📁 目录结构检查:")
    for dir_path in required_dirs:
        if Path(dir_path).is_dir():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ❌ {dir_path}/")
            missing_required.append(f"{dir_path}/")
    
    for dir_path in optional_dirs:
        if Path(dir_path).is_dir():
            print(f"  ✅ {dir_path}/")
        else:
            print(f"  ➖ {dir_path}/ (可选)")
    
    # 统计结果
    print(f"\n📊 结构检查统计:")
    print(f"  ✅ 必需文件: {len(existing_required)}/{len(required_files)}")
    print(f"  ✅ 可选文件: {len(existing_optional)}/{len(optional_files)}")
    
    if missing_required:
        print(f"\n⚠️  缺失的必需文件/目录:")
        for item in missing_required:
            print(f"    - {item}")
        return False
    
    print(f"\n🎉 项目结构完整！")
    return True

def test_python_imports():
    """测试Python模块导入"""
    print("\n🐍 测试Python模块导入...")
    
    # 基础导入测试
    import_tests = [
        # 数据结构
        ("数据结构", "from src.models.data_structures import DiscussantInitialOutput, ScoreSheet, DiscussantFinalOutput, RefereeAnalysis"),
        
        # 提供器
        ("基础提供器", "from src.providers.base import ModelProvider"),
        ("模拟提供器", "from src.providers.mock_provider import MockModelProvider"),
        
        # 核心模块
        ("编排器", "from src.core.orchestrator import NGTOrchestrator"),
        ("解析器", "from src.core.parser import DataParser"),
        ("状态追踪", "from src.core.state_tracker import StateTracker"),
        
        # 工具模块
        ("日志工具", "from src.utils.logger import setup_logger, NGTLogger"),
        ("结果呈现", "from src.utils.presenter import ResultPresenter"),
        
        # 主程序
        ("主程序", "from ngt_ai_mvp import NGTDecisionApp")
    ]
    
    success_count = 0
    total_count = len(import_tests)
    failed_imports = []
    
    for name, import_statement in import_tests:
        try:
            exec(import_statement)
            print(f"  ✅ {name}")
            success_count += 1
        except ImportError as e:
            print(f"  ❌ {name}: {e}")
            failed_imports.append((name, str(e)))
        except Exception as e:
            print(f"  ⚠️  {name}: {e}")
            failed_imports.append((name, str(e)))
    
    print(f"\n📊 导入测试结果:")
    print(f"  成功: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    if failed_imports:
        print(f"\n❌ 导入失败详情:")
        for name, error in failed_imports:
            print(f"    {name}: {error}")
        return False
    
    return True

def test_basic_functionality():
    """测试基本功能"""
    print("\n🔧 测试基本功能...")
    
    try:
        # 测试数据结构创建
        print("  🔍 测试数据结构...")
        from src.models.data_structures import DiscussantInitialOutput, ScoreRecord, ScoreSheet
        
        output = DiscussantInitialOutput("AI_1", "test-model", "test conclusion")
        assert output.ai_id == "AI_1"
        assert output.model_name == "test-model"
        
        score_record = ScoreRecord(4, "good point")
        assert score_record.score == 4
        
        print("    ✅ 数据结构创建正常")
        
        # 测试模拟提供器
        print("  🔍 测试模拟提供器...")
        from src.providers.mock_provider import MockModelProvider
        
        provider = MockModelProvider("test-model", "AI_TEST")
        assert provider.get_model_name() == "test-model"
        assert provider.get_ai_id() == "AI_TEST"
        
        print("    ✅ 模拟提供器创建正常")
        
        # 测试状态追踪
        print("  🔍 测试状态追踪...")
        from src.core.state_tracker import StateTracker
        
        tracker = StateTracker()
        tracker.start_process("test question")
        assert tracker.user_question == "test question"
        assert tracker.current_stage == "阶段1-独立观点生成"
        
        print("    ✅ 状态追踪功能正常")
        
        # 测试数据解析
        print("  🔍 测试数据解析...")
        from src.core.parser import DataParser
        
        json_data = '{"ai_id": "AI_1", "model_name": "gpt-4", "conclusion": "test conclusion"}'
        result = DataParser.parse_initial_output(json_data)
        assert result is not None
        assert result.ai_id == "AI_1"
        
        print("    ✅ 数据解析功能正常")
        
        # 测试结果呈现
        print("  🔍 测试结果呈现...")
        from src.utils.presenter import ResultPresenter
        
        test_result = {
            "question": "test question", 
            "process_duration": "1.5秒",
            "participants": {"total": 5, "discussants": 4, "referee": 1},
            "total_stages": 6,
            "initial_ideas": [],
            "final_decisions": [],
            "referee_analysis": None,
            "statistics": {
                "total_ideas": 0,
                "revised_count": 0, 
                "defended_count": 0,
                "average_score": 0,
                "completion_rate": 1.0,
                "error_count": 0
            }
        }
        
        formatted = ResultPresenter.format_result(test_result)
        assert len(formatted) > 100  # 确保有实际内容
        assert "NGT-AI" in formatted
        
        print("    ✅ 结果呈现功能正常")
        
        # 测试主程序类
        print("  🔍 测试主程序类...")
        from ngt_ai_mvp import NGTDecisionApp
        
        app = NGTDecisionApp(use_real_apis=False)
        info = app.get_system_info()
        assert "version" in info
        assert "discussants_count" in info
        
        print("    ✅ 主程序类创建正常")
        
        return True
        
    except Exception as e:
        print(f"    ❌ 功能测试失败: {e}")
        import traceback
        print(f"    详细错误: {traceback.format_exc()}")
        return False

def test_environment():
    """测试运行环境"""
    print("🌍 检查运行环境...")
    
    # Python版本检查
    python_version = sys.version_info
    print(f"  🐍 Python版本: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version < (3, 8):
        print("  ❌ Python版本过低，需要3.8或更高版本")
        return False
    else:
        print("  ✅ Python版本满足要求")
    
    # 检查工作目录
    current_dir = Path.cwd()
    print(f"  📁 当前目录: {current_dir}")
    
    # 检查是否在项目根目录
    if not Path("ngt_ai_mvp.py").exists():
        print("  ⚠️  当前目录可能不是项目根目录")
        return False
    
    print("  ✅ 工作目录正确")
    
    # 检查权限
    try:
        test_file = Path("test_write_permission.tmp")
        test_file.write_text("test")
        test_file.unlink()
        print("  ✅ 文件写入权限正常")
    except Exception as e:
        print(f"  ❌ 文件写入权限异常: {e}")
        return False
    
    return True

def create_missing_directories():
    """创建缺失的目录"""
    print("\n📁 创建必要目录...")
    
    required_dirs = ["logs", "output", "data"]
    
    for dir_name in required_dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            try:
                dir_path.mkdir(parents=True, exist_ok=True)
                print(f"  ✅ 创建目录: {dir_name}/")
            except Exception as e:
                print(f"  ❌ 创建目录失败 {dir_name}: {e}")
        else:
            print(f"  ✅ 目录已存在: {dir_name}/")

def run_comprehensive_test():
    """运行综合测试"""
    print("🧪 NGT-AI 项目综合测试")
    print("=" * 60)
    
    test_results = {}
    
    # 环境测试
    test_results["environment"] = test_environment()
    
    # 结构测试
    test_results["structure"] = test_project_structure()
    
    # 导入测试
    test_results["imports"] = test_python_imports()
    
    # 功能测试
    test_results["functionality"] = test_basic_functionality()
    
    # 创建目录
    create_missing_directories()
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 测试结果总结")
    print("=" * 60)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name.title():<15}: {status}")
    
    print(f"\n🎯 总体结果: {passed_tests}/{total_tests} 测试通过 ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 恭喜！所有测试通过，项目已准备就绪")
        print("\n🚀 可以使用以下命令启动系统:")
        print("   • python ngt_ai_mvp.py  (直接启动)")
        print("   • python run.py         (交互式启动)")
        
        if Path("start.bat").exists():
            print("   • start.bat             (Windows一键启动)")
        
        return True
    else:
        print(f"\n⚠️  存在 {total_tests - passed_tests} 个问题需要解决")
        print("\n💡 建议:")
        
        if not test_results["structure"]:
            print("   1. 检查项目文件是否完整创建")
        if not test_results["imports"]:
            print("   2. 检查Python文件内容是否正确")
        if not test_results["functionality"]:
            print("   3. 检查代码逻辑是否有误")
        
        return False

def quick_test():
    """快速测试(只测试关键项目)"""
    print("⚡ NGT-AI 快速测试")
    print("=" * 30)
    
    # 检查关键文件
    key_files = ["ngt_ai_mvp.py", "src/core/orchestrator.py", "src/providers/mock_provider.py"]
    missing_key_files = [f for f in key_files if not Path(f).exists()]
    
    if missing_key_files:
        print(f"❌ 缺少关键文件: {missing_key_files}")
        return False
    
    print("✅ 关键文件存在")
    
    # 快速导入测试
    try:
        from ngt_ai_mvp import NGTDecisionApp
        print("✅ 主程序可导入")
    except Exception as e:
        print(f"❌ 主程序导入失败: {e}")
        return False
    
    print("🎉 快速测试通过！")
    return True

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='NGT-AI 项目测试工具')
    parser.add_argument('--quick', action='store_true', help='运行快速测试')
    parser.add_argument('--structure', action='store_true', help='仅测试项目结构')
    parser.add_argument('--imports', action='store_true', help='仅测试模块导入')
    parser.add_argument('--function', action='store_true', help='仅测试基本功能')
    
    args = parser.parse_args()
    
    # Windows控制台编码设置
    if os.name == 'nt':
        os.system('chcp 65001 > nul 2>&1')
    
    try:
        if args.quick:
            success = quick_test()
        elif args.structure:
            success = test_project_structure()
        elif args.imports:
            success = test_python_imports()
        elif args.function:
            success = test_basic_functionality()
        else:
            success = run_comprehensive_test()
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⛔ 测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试过程发生错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()