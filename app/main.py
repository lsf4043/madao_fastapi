# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.api.v1.api import api_router
from app.core.config import settings

app = FastAPI(
    title="财经新闻爬取系统",
    description="爬取财经新闻资讯的FastAPI项目",
    version="1.0.0"
)

# 包含API路由
app.include_router(api_router, prefix="/api/v1")

# 挂载静态文件
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """返回登录页面"""
    with open("app/static/login.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "ok", "message": "服务运行正常"}
