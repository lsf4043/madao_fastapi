# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """应用配置"""
    PROJECT_NAME: str = "财经新闻爬取系统"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-in-production-2024"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS配置
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./finance_news.db"

    class Config:
        case_sensitive = True


settings = Settings()
