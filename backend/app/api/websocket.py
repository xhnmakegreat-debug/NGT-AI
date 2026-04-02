"""
WebSocket实时通信
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.websocket("/ws/decision")
async def websocket_decision(websocket: WebSocket):
    """实时决策分析WebSocket"""
    await websocket.accept()
    logger.info("WebSocket连接已建立")
    
    try:
        while True:
            # 接收消息
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # 发送进度更新示例
            await websocket.send_json({
                "type": "progress",
                "stage": "独立观点生成",
                "progress": 20
            })
            
            # TODO: 实际处理逻辑
            
    except WebSocketDisconnect:
        logger.info("WebSocket连接已断开")