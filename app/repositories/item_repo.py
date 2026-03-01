# -*- coding: utf-8 -*-
"""
商品数据访问层 (Repository)
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.item import Item


class ItemRepository:
    """商品数据访问"""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, item_id: int) -> Optional[Item]:
        """根据 ID 获取商品"""
        return self.db.query(Item).filter(Item.id == item_id).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """获取商品列表"""
        return self.db.query(Item).offset(skip).limit(limit).all()

    def get_count(self) -> int:
        """获取商品总数"""
        return self.db.query(Item).count()

    def create(self, item: Item) -> Item:
        """创建商品"""
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def update(self, item: Item) -> Item:
        """更新商品"""
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: Item) -> bool:
        """删除商品"""
        self.db.delete(item)
        self.db.commit()
        return True
