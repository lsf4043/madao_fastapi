# -*- coding: utf-8 -*-
"""
商品业务逻辑层 (Service)
"""
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.repositories.item_repo import ItemRepository


class ItemService:
    """商品业务逻辑"""

    def __init__(self, db: Session):
        self.db = db
        self.repository = ItemRepository(db)

    def get_by_id(self, item_id: int) -> Optional[ItemResponse]:
        """根据 ID 获取商品"""
        item = self.repository.get_by_id(item_id)
        if item:
            return self._to_response(item)
        return None

    def get_items(self, skip: int = 0, limit: int = 100) -> List[ItemResponse]:
        """获取商品列表"""
        items = self.repository.get_all(skip=skip, limit=limit)
        return [self._to_response(item) for item in items]

    def get_count(self) -> int:
        """获取商品总数"""
        return self.repository.get_count()

    def create(self, item_in: ItemCreate) -> ItemResponse:
        """创建商品"""
        item = Item(
            name=item_in.name,
            description=item_in.description,
            price=item_in.price,
            tax=item_in.tax
        )
        item = self.repository.create(item)
        return self._to_response(item)

    def update(self, item_id: int, item_in: ItemUpdate) -> Optional[ItemResponse]:
        """更新商品"""
        item = self.repository.get_by_id(item_id)
        if not item:
            return None

        update_data = item_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(item, field, value)

        item = self.repository.update(item)
        return self._to_response(item)

    def delete(self, item_id: int) -> bool:
        """删除商品"""
        item = self.repository.get_by_id(item_id)
        if not item:
            return False
        return self.repository.delete(item)

    def _to_response(self, item: Item) -> ItemResponse:
        """转换为响应模型"""
        price_with_tax = item.price + item.tax if item.tax else item.price
        return ItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            tax=item.tax,
            price_with_tax=price_with_tax
        )
