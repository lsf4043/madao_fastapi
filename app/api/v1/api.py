# -*- coding: utf-8 -*-
"""
API v1 路由汇总
"""
from fastapi import APIRouter
from app.api.v1.endpoints import items, game

api_router = APIRouter()

# 注册子路由
api_router.include_router(items.router)
api_router.include_router(game.router)
