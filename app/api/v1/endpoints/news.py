# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_db
from app.api.v1.endpoints.auth import get_current_user
from app.models import User
from app.services.news_crawler import news_crawler
from pydantic import BaseModel, Field

router = APIRouter()


class NewsItem(BaseModel):
    """新闻项模型"""
    title: str = Field(..., description="新闻标题")
    url: str = Field(..., description="新闻链接")
    source: str = Field(..., description="新闻来源")
    publish_time: Optional[str] = Field(None, description="发布时间")
    summary: Optional[str] = Field(None, description="新闻摘要")


class NewsListResponse(BaseModel):
    """新闻列表响应"""
    total: int = Field(..., description="总数")
    items: List[NewsItem] = Field(..., description="新闻列表")


@router.get("/list", response_model=NewsListResponse)
async def get_news_list(
    source: Optional[str] = Query(None, description="新闻来源过滤"),
    limit: int = Query(10, ge=1, le=50, description="返回数量限制"),
    current_user: User = Depends(get_current_user)
):
    """获取新闻列表（需要登录）"""
    # 爬取新闻
    all_news = await news_crawler.crawl_all_sources()

    # 按来源过滤
    if source:
        all_news = [n for n in all_news if n.get('source') == source]

    # 限制数量
    news_items = all_news[:limit]

    return NewsListResponse(
        total=len(all_news),
        items=[NewsItem(**item) for item in news_items]
    )


@router.post("/crawl")
async def crawl_news(current_user: User = Depends(get_current_user)):
    """手动触发爬取新闻（需要登录）"""
    try:
        news = await news_crawler.crawl_all_sources()
        return {
            "message": f"成功爬取 {len(news)} 条新闻",
            "count": len(news),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"爬取失败: {str(e)}"
        )


@router.get("/source/{source_name}")
async def get_news_by_source(
    source_name: str,
    current_user: User = Depends(get_current_user)
):
    """按来源获取新闻"""
    if source_name == "sina":
        news = await news_crawler.crawl_sina_finance()
    elif source_name == "eastmoney":
        news = await news_crawler.crawl_eastmoney()
    else:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的数据源: {source_name}"
        )

    return {
        "source": source_name,
        "count": len(news),
        "items": news
    }
