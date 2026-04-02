# NGT-AI 后端服务

基于FastAPI的NGT-AI决策系统后端服务。

## 功能特性

- 🏥 健康检查API
- 🤖 决策分析API  
- 🔌 WebSocket实时通信
- 📊 决策状态跟踪
- 🎯 结果查询接口

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
# 方式1: 使用启动脚本
python start_server.py

# 方式2: 直接运行
python -m backend.app.main

# 方式3: 使用uvicorn
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 访问服务

- 🌐 服务地址: ://localhost:8000http
- 📚 API文档: http://localhost:8000/docs
- 🔍 健康检查: http://localhost:8000/api/health

## API接口

### 健康检查
```
GET /api/health
```

### 决策分析
```
POST /api/decision/analyze
{
    "question": "决策问题",
    "context": "背景信息",
    "options": ["选项1", "选项2"],
    "criteria": ["标准1", "标准2"]
}
```

### 决策状态
```
GET /api/decision/status/{decision_id}
```

### 决策结果
```
GET /api/decision/result/{decision_id}
```

### WebSocket连接
```
WS /api/ws/decision
```

## 配置说明

配置文件位于 `app/config.py`，支持以下配置项：

- `host`: 服务监听地址 (默认: 0.0.0.0)
- `port`: 服务端口 (默认: 8000)
- `debug`: 调试模式 (默认: True)
- `cors_origins`: CORS允许的源 (默认: ["*"])

## 开发说明

### 项目结构
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI应用入口
│   ├── config.py        # 配置管理
│   ├── api/            # API路由
│   │   ├── health.py   # 健康检查
│   │   ├── decision.py # 决策分析
│   │   └── websocket.py # WebSocket
│   ├── models/         # 数据模型
│   └── services/       # 业务服务
├── requirements.txt    # 依赖包
├── start_server.py    # 启动脚本
└── README.md          # 说明文档
```

### 添加新的API接口

1. 在 `app/api/` 目录下创建新的路由文件
2. 在 `app/main.py` 中注册路由
3. 更新此README文档

### 环境变量

可以通过环境变量覆盖配置：

```bash
export NGT_HOST=0.0.0.0
export NGT_PORT=8000
export NGT_DEBUG=true
```

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   netstat -ano | findstr :8000
   # 杀死进程
   taskkill /PID <PID> /F
   ```

2. **依赖安装失败**
   ```bash
   # 升级pip
   python -m pip install --upgrade pip
   # 重新安装依赖
   pip install -r requirements.txt --force-reinstall
   ```

3. **CORS错误**
   - 检查 `config.py` 中的 `cors_origins` 配置
   - 确保前端地址在允许列表中

### 日志查看

服务运行时会输出详细日志，包括：
- 请求处理日志
- 错误信息
- 性能指标

## 部署说明

### 生产环境部署

1. 设置环境变量
   ```bash
   export NGT_DEBUG=false
   export NGT_CORS_ORIGINS=["https://yourdomain.com"]
   ```

2. 使用生产级WSGI服务器
   ```bash
   pip install gunicorn
   gunicorn backend.app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

3. 配置反向代理 (Nginx)
   ```nginx
   location / {
       proxy_pass http://127.0.0.1:8000;
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
   }
   ```

## 许可证

MIT License
