# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models import User
from pydantic import BaseModel

router = APIRouter()


class NewsItem(BaseModel):
    """新闻项模型"""
    title: str
    url: str
    source: str
    publish_time: str = None
    summary: str = None


@router.get("/list", response_model=List[NewsItem])
def get_news_list(
    source: str = None,
    limit: int = 10,
    current_user: User = Depends(get_current_user)
):
    """获取新闻列表（需要登录）"""
    # 这里暂时返回模拟数据，后续实现爬虫功能
    mock_news = [
        NewsItem(
            title="央行：稳健的货币政策要灵活精准、合理适度",
            url="https://finance.example.com/news/1",
            source="央行官网",
            publish_time="2024-01-15 10:30:00",
            summary="中国人民银行发布最新货币政策执行报告..."
        ),
        NewsItem(
            title="A股三大指数集体收涨，北向资金净流入超百亿",
            url="https://finance.example.com/news/2",
            source="证券时报",
            publish_time="2024-01-15 15:00:00",
            summary="今日A股市场表现强劲，三大指数全线收涨..."
        ),
        NewsItem(
            title="证监会：持续深化资本市场改革",
            url="https://finance.example.com/news/3",
            source="证监会官网",
            publish_time="2024-01-15 09:00:00",
            summary="证监会召开新闻发布会，介绍资本市场改革进展..."
        )
    ]

    if source:
        mock_news = [n for n in mock_news if n.source == source]

    return mock_news[:limit]


@router.get("/crawl")
def crawl_news(current_user: User = Depends(get_current_user)):
    """爬取新闻（需要登录）"""
    # 这里后续实现爬虫功能
    return {
        "message": "新闻爬取功能开发中",
        "status": "pending"
    }
