# -*- coding: utf-8 -*-
from fastapi import APIRouter
from app.api.v1.endpoints import auth, news

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(news.router, prefix="/news", tags=["新闻"])
