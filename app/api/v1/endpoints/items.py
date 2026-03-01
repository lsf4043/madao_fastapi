# -*- coding: utf-8 -*-
"""
商品 API 端点
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.api.deps import get_database
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, ItemListResponse
from app.services.item_service import ItemService

router = APIRouter(prefix="/items", tags=["商品管理"])


@router.get("/", response_model=ItemListResponse, summary="获取商品列表")
def list_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database)
):
    """获取商品列表"""
    service = ItemService(db)
    items = service.get_items(skip=skip, limit=limit)
    total = service.get_count()
    return ItemListResponse(items=items, total=total)


@router.get("/{item_id}", response_model=ItemResponse, summary="获取单个商品")
def get_item(
    item_id: int,
    db: Session = Depends(get_database)
):
    """根据 ID 获取商品"""
    service = ItemService(db)
    item = service.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"商品 ID {item_id} 不存在"
        )
    return item


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED, summary="创建商品")
def create_item(
    item_in: ItemCreate,
    db: Session = Depends(get_database)
):
    """创建新商品"""
    service = ItemService(db)
    return service.create(item_in)


@router.put("/{item_id}", response_model=ItemResponse, summary="更新商品")
def update_item(
    item_id: int,
    item_in: ItemUpdate,
    db: Session = Depends(get_database)
):
    """更新商品信息"""
    service = ItemService(db)
    item = service.update(item_id, item_in)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"商品 ID {item_id} 不存在"
        )
    return item


@router.delete("/{item_id}", summary="删除商品")
def delete_item(
    item_id: int,
    db: Session = Depends(get_database)
):
    """删除商品"""
    service = ItemService(db)
    success = service.delete(item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"商品 ID {item_id} 不存在"
        )
    return {"message": f"商品 ID {item_id} 删除成功"}
