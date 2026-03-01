# -*- coding: utf-8 -*-
"""
API 依赖注入
"""
from typing import Generator
from sqlalchemy.orm import Session
from app.database import get_db


def get_database() -> Generator[Session, None, None]:
    """获取数据库会话"""
    yield from get_db()
