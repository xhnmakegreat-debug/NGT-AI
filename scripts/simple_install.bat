@echo off
chcp 65001 >nul
title NGT-AI 简化安装

echo ========================================
echo   NGT-AI 系统 - 快速安装
echo ========================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装，请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✅ Python环境正常
python --version

REM 删除旧环境（如果存在）
if exist venv (
    echo 🗑️ 删除旧虚拟环境...
    rmdir /s /q venv
)

REM 创建虚拟环境
echo 🔨 创建虚拟环境...
python -m venv venv
if errorlevel 1 (
    echo ❌ 创建失败
    pause
    exit /b 1
)

REM 激活环境
echo 🔧 激活环境...
call venv\Scripts\activate.bat

REM 升级pip
echo 📦 升级pip...
python -m pip install --upgrade pip

REM 安装依赖
echo.
echo 选择安装模式:
echo 1 = 最小模式（仅测试）
echo 2 = 完整模式（包含API）
echo.
set /p choice=输入数字: 

if "%choice%"=="1" goto minimal
if "%choice%"=="2" goto full

:minimal
echo 🚀 安装测试依赖...
pip install colorama
echo ✅ 最小依赖安装完成
goto end

:full
echo 🚀 安装完整依赖...
if exist requirements.txt (
    pip install -r requirements.txt
    echo ✅ 完整依赖安装完成
) else (
    echo ❌ requirements.txt 不存在
    echo 安装基础包...
    pip install colorama openai anthropic httpx pydantic pyyaml
    echo ✅ 基础依赖安装完成
)

:end
echo.
echo 📋 验证安装:
python -c "print('✅ Python工作正常')"
python -c "import asyncio; print('✅ asyncio可用')"

echo.
echo ========================================
echo ✅ 安装完成！
echo.
echo 使用方法:
echo 1. python ngt_ai_mvp.py
echo 2. python run.py  
echo 3. 双击 start.bat
echo ========================================
pause