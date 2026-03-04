# -*- coding: utf-8 -*-
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=20, description="用户名长度3-20个字符")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")


class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6, max_length=50, description="密码长度6-50个字符")

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """验证用户名"""
        if not v:
            raise ValueError('用户名不能为空')
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """验证密码"""
        if not v:
            raise ValueError('密码不能为空')
        if len(v) < 6:
            raise ValueError('密码长度至少6个字符')
        return v


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
