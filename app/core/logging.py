# -*- coding: utf-8 -*-
"""
日志配置
"""
import logging
import sys
from app.core.config import settings


def setup_logging() -> logging.Logger:
    """配置日志"""
    logger = logging.getLogger("madao")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))

    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger


logger = setup_logging()
