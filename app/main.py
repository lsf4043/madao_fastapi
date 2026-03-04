# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from app.api.v1.api import api_router
from app.core.config import settings
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时初始化数据库
    await init_db()
    yield
    # 关闭时清理资源


app = FastAPI(
    title="财经新闻爬取系统",
    description="爬取财经新闻资讯的FastAPI项目",
    version="1.0.0",
    lifespan=lifespan
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """全局验证错误处理器"""
    errors = exc.errors()
    error_messages = []

    for error in errors:
        field = error.get('loc', ['未知字段'])[-1]
        message = error.get('msg', '验证失败')

        # 转换字段名为中文
        field_names = {
            'username': '用户名',
            'password': '密码',
            'email': '邮箱'
        }
        field_cn = field_names.get(field, field)

        # 转换错误消息为中文
        message_cn = message
        if 'at least' in message.lower():
            message_cn = f"长度至少为{message.split()[-2]}个字符"
        elif 'at most' in message.lower():
            message_cn = f"长度最多为{message.split()[-2]}个字符"
        elif 'not a valid email' in message.lower():
            message_cn = "邮箱格式不正确"

        error_messages.append(f"{field_cn}: {message_cn}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "; ".join(error_messages)}
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
