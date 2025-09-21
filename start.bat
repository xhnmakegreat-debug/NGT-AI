@echo off
chcp 65001 >nul 2>&1
title NGT-AI 多智能体协作决策系统

echo.
echo ================================================================
echo     🎯 NGT-AI 多智能体协作决策系统 v2.0
echo ================================================================
echo                 基于名义小组技术的AI集体决策平台
echo ================================================================
echo.

REM 检查Python环境
echo 🔍 检查运行环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或未添加到PATH
    echo.
    echo 💡 解决方案:
    echo    1. 下载安装Python 3.8+: https://www.python.org/downloads/
    echo    2. 安装时勾选 "Add Python to PATH"
    echo    3. 重新打开命令行
    echo.
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ 检测到Python: %PYTHON_VERSION%

REM 检查核心文件
echo 🔍 检查项目文件...
if not exist "ngt_ai_mvp.py" (
    echo ❌ 缺少主程序文件: ngt_ai_mvp.py
    echo 💡 请确保所有项目文件都已正确创建
    pause
    exit /b 1
)

if not exist "src\core\orchestrator.py" (
    echo ❌ 缺少核心模块文件
    echo 💡 请检查src目录下的文件是否完整
    pause
    exit /b 1
)

echo ✅ 项目文件检查通过

REM 检查虚拟环境
if exist "venv\Scripts\activate.bat" (
    echo 🔧 发现虚拟环境，正在激活...
    call venv\Scripts\activate.bat
    if errorlevel 1 (
        echo ⚠️  虚拟环境激活失败，使用系统Python
    ) else (
        echo ✅ 虚拟环境已激活
    )
) else (
    echo ℹ️  未发现虚拟环境，使用系统Python
)

REM 运行项目结构测试
echo 🧪 快速验证项目结构...
python test_imports.py --quick >nul 2>&1
if errorlevel 1 (
    echo ⚠️  项目结构可能不完整，但尝试继续运行...
) else (
    echo ✅ 项目结构验证通过
)

REM 启动主程序
echo.
echo 🚀 启动NGT-AI决策系统...
echo ================================================================
echo.

python run.py

REM 程序结束处理
echo.
echo ================================================================
echo 📊 会话结束统计
echo ================================================================

REM 检查输出文件
if exist "output\*.txt" (
    for /f %%i in ('dir /b output\*.txt 2^>nul ^| find /c /v ""') do set FILE_COUNT=%%i
    echo 💾 本次生成了 %FILE_COUNT% 个决策报告文件
    echo 📁 文件保存位置: output\ 目录
) else (
    echo 📝 本次未保存决策报告文件
)

REM 检查日志
if exist "logs\*.log" (
    echo 📋 系统日志已保存到 logs\ 目录
) else (
    echo ℹ️  未生成系统日志
)

echo.
echo 感谢使用NGT-AI多智能体协作决策系统！
echo 如有问题或建议，请查看README.md或联系开发团队
echo.
echo ================================================================
pause
