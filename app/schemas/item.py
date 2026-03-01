# -*- coding: utf-8 -*-
"""
Item Pydantic Schemas (请求/响应模型)
"""
from pydantic import BaseModel, Field
from typing import Optional


class ItemBase(BaseModel):
    """商品基础模型"""
    name: str = Field(..., min_length=1, max_length=100, description="商品名称")
    description: Optional[str] = Field(None, description="商品描述")
    price: float = Field(..., gt=0, description="商品价格")
    tax: Optional[float] = Field(None, ge=0, description="税费")


class ItemCreate(ItemBase):
    """创建商品请求模型"""
    pass


class ItemUpdate(ItemBase):
    """更新商品请求模型"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)


class ItemResponse(ItemBase):
    """商品响应模型"""
    id: int
    price_with_tax: Optional[float] = Field(None, description="含税价格")

    class Config:
        from_attributes = True


class ItemListResponse(BaseModel):
    """商品列表响应模型"""
    items: list[ItemResponse]
    total: int
