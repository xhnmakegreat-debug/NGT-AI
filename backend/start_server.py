#!/usr/bin/env python3
"""
NGT-AI 后端服务器启动脚本
"""
import uvicorn
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(project_root))

from backend.app.main import app
from backend.app.config import settings

if __name__ == "__main__":
    print("🚀 启动 NGT-AI 后端服务器...")
    print(f"📍 服务地址: http://{settings.host}:{settings.port}")
    print(f"📚 API文档: http://{settings.host}:{settings.port}/docs")
    print(f"🔍 健康检查: http://{settings.host}:{settings.port}/api/health")
    
    uvicorn.run(
        "backend.app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
