@echo off
chcp 65001 >nul 2>&1
title NGT-AI 快速测试

echo ===============================================
echo    🧪 NGT-AI 系统快速测试
echo ===============================================
echo.

REM 测试Python环境
echo 🔍 检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python环境不可用
    echo.
    echo 💡 请先安装Python 3.8+
    echo https://www.python.org/downloads/
    goto :error
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION%

REM 检查核心文件
echo.
echo 🔍 检查核心项目文件...

set MISSING_FILES=0

if not exist "ngt_ai_mvp.py" (
    echo ❌ 缺少主程序: ngt_ai_mvp.py
    set /a MISSING_FILES+=1
) else (
    echo ✅ 主程序文件存在
)

if not exist "src\core\orchestrator.py" (
    echo ❌ 缺少核心模块: src\core\orchestrator.py
    set /a MISSING_FILES+=1
) else (
    echo ✅ 核心编排器存在
)

if not exist "src\providers\mock_provider.py" (
    echo ❌ 缺少模拟器: src\providers\mock_provider.py
    set /a MISSING_FILES+=1
) else (
    echo ✅ AI模拟器存在
)

if not exist "src\models\data_structures.py" (
    echo ❌ 缺少数据结构: src\models\data_structures.py
    set /a MISSING_FILES+=1
) else (
    echo ✅ 数据结构文件存在
)

if %MISSING_FILES% gtr 0 (
    echo.
    echo ❌ 发现 %MISSING_FILES% 个缺失文件
    goto :error
)

REM 测试Python导入
echo.
echo 🔍 测试Python模块导入...

REM 测试主程序导入
python -c "from ngt_ai_mvp import NGTDecisionApp; print('✅ 主程序导入成功')" 2>nul
if errorlevel 1 (
    echo ❌ 主程序导入失败
    echo.
    echo 💡 可能原因:
    echo    1. Python文件内容有误
    echo    2. 依赖模块缺失
    echo    3. 语法错误
    goto :error
)

REM 测试基础模块导入
python -c "from src.providers.mock_provider import MockModelProvider; print('✅ AI模拟器正常')" 2>nul
if errorlevel 1 (
    echo ❌ AI模拟器导入失败
    goto :error
)

python -c "from src.core.orchestrator import NGTOrchestrator; print('✅ 核心编排器正常')" 2>nul
if errorlevel 1 (
    echo ❌ 核心编排器导入失败
    goto :error
)

REM 测试基本功能
echo.
echo 🔍 测试基本功能...
python -c "from ngt_ai_mvp import NGTDecisionApp; app = NGTDecisionApp(); info = app.get_system_info(); print('✅ 系统信息:', info['version'])" 2>nul
if errorlevel 1 (
    echo ❌ 基本功能测试失败
    goto :error
)

REM 检查虚拟环境（可选）
echo.
echo 🔍 检查环境配置...
if exist "venv\Scripts\activate.bat" (
    echo ✅ 发现虚拟环境
) else (
    echo ℹ️  未使用虚拟环境 (使用系统Python)
)

REM 检查配置文件（可选）
if exist "config.yaml" (
    echo ✅ 配置文件存在
) else (
    echo ⚠️  配置文件缺失 (使用默认设置)
)

REM 检查依赖文件（可选）
if exist "requirements.txt" (
    echo ✅ 依赖文件存在
) else (
    echo ⚠️  依赖文件缺失
)

echo.
echo ===============================================
echo 🎉 快速测试全部通过！
echo ===============================================
echo.
echo 📊 系统状态:
echo    ✅ Python环境正常
echo    ✅ 项目文件完整
echo    ✅ 模块导入成功
echo    ✅ 基本功能正常
echo.
echo 🚀 可以使用以下命令启动系统:
echo    1. start.bat           (推荐，图形化启动)
echo    2. python run.py       (交互式启动)
echo    3. python ngt_ai_mvp.py (直接启动)
echo.
echo 📖 更详细的测试可以运行:
echo    python test_imports.py
echo ===============================================

pause
exit /b 0

:error
echo.
echo ===============================================
echo ❌ 快速测试失败！
echo ===============================================
echo.
echo 🔧 建议的解决步骤:
echo    1. 运行 python test_imports.py 获取详细信息
echo    2. 检查项目文件是否完整
echo    3. 重新安装依赖: simple_install.bat
echo    4. 查看 README.md 获取帮助
echo.
echo 💡 如果问题持续存在:
echo    - 确保所有项目文件都已正确创建
echo    - 检查Python版本 (需要3.8+)
echo    - 确认在正确的项目目录中
echo ===============================================

pause
exit /b 1