"""
日志工具模块
提供统一的日志配置和管理
"""

import logging
import os
from pathlib import Path
from typing import Optional

def setup_logger(
    name: str = "ngt-ai",
    level: str = "INFO",
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径
        console_output: 是否输出到控制台
        
    Returns:
        配置好的日志记录器
    """
    logger = logging.getLogger(name)
    
    # 如果已经配置过，直接返回
    if logger.handlers:
        return logger
    
    # 设置日志级别
    log_level = getattr(logging, level.upper(), logging.INFO)
    logger.setLevel(log_level)
    
    # 创建格式器
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 控制台处理器
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 文件处理器
    if log_file:
        # 确保日志目录存在
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def get_logger(name: str = "ngt-ai") -> logging.Logger:
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
        
    Returns:
        日志记录器
    """
    return logging.getLogger(name)

class NGTLogger:
    """NGT系统专用日志类"""
    
    def __init__(self, name: str = "ngt-ai"):
        self.logger = setup_logger(
            name=name,
            level="INFO",
            log_file="logs/ngt_ai.log",
            console_output=True
        )
    
    def log_stage_start(self, stage: str, details: str = ""):
        """记录阶段开始"""
        message = f"🚀 {stage} 开始"
        if details:
            message += f" - {details}"
        self.logger.info(message)
    
    def log_stage_complete(self, stage: str, duration: float = None, results_count: int = None):
        """记录阶段完成"""
        message = f"✅ {stage} 完成"
        if duration is not None:
            message += f" - 耗时: {duration:.2f}秒"
        if results_count is not None:
            message += f" - 结果数量: {results_count}"
        self.logger.info(message)
    
    def log_error(self, component: str, error: Exception, context: str = ""):
        """记录错误"""
        message = f"❌ {component} 错误: {str(error)}"
        if context:
            message += f" - 上下文: {context}"
        self.logger.error(message)
    
    def log_api_call(self, provider: str, model: str, tokens_used: int = None):
        """记录API调用"""
        message = f"🔌 API调用: {provider} ({model})"
        if tokens_used:
            message += f" - Token使用量: {tokens_used}"
        self.logger.debug(message)
    
    def log_retry(self, component: str, attempt: int, max_attempts: int, reason: str = ""):
        """记录重试"""
        message = f"🔄 {component} 重试 ({attempt}/{max_attempts})"
        if reason:
            message += f" - 原因: {reason}"
        self.logger.warning(message)
    
    def log_performance(self, operation: str, duration: float, details: dict = None):
        """记录性能信息"""
        message = f"⚡ 性能: {operation} - {duration:.3f}秒"
        if details:
            detail_str = ", ".join(f"{k}: {v}" for k, v in details.items())
            message += f" - {detail_str}"
        self.logger.info(message)

# 全局日志实例
ngt_logger = NGTLogger()
