# -*- coding: utf-8 -*-
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, Token
from app.core.security import verify_password, get_password_hash, create_access_token, decode_token
from app.core.config import settings
from datetime import timedelta
from typing import AsyncGenerator
from pydantic import ValidationError

router = APIRouter()
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )
    username: str = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )

    result = await db.execute(select(User).where(User.username == username))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """用户注册"""
    try:
        # 检查用户名是否已存在
        result = await db.execute(select(User).where(User.username == user_create.username))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已被使用，请选择其他用户名"
            )

        # 检查邮箱是否已存在
        if user_create.email:
            result = await db.execute(select(User).where(User.email == user_create.email))
            if result.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该邮箱已被注册，请使用其他邮箱"
                )

        # 创建新用户
        hashed_password = get_password_hash(user_create.password)
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user

    except ValidationError as e:
        # 处理Pydantic验证错误
        errors = e.errors()
        error_messages = []
        for error in errors:
            field = error.get('loc', ['未知字段'])[-1]
            message = error.get('msg', '验证失败')
            error_messages.append(f"{field}: {message}")

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="; ".join(error_messages)
        )


@router.post("/login", response_model=Token)
async def login(
    user_login: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """用户登录"""
    # 查找用户
    result = await db.execute(select(User).where(User.username == user_login.username))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 验证密码
    if not verify_password(user_login.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 检查用户是否激活
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已被禁用"
        )

    # 创建访问令牌
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user
