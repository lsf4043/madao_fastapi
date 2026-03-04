# -*- coding: utf-8 -*-
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""
    username: str
    email: Optional[EmailStr] = None


class UserCreate(UserBase):
    """用户创建模型"""
    password: str


class UserLogin(BaseModel):
    """用户登录模型"""
    username: str
    password: str


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """令牌模型"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """令牌数据"""
    username: Optional[str] = None
