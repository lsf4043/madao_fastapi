# -*- coding: utf-8 -*-
"""
Item 数据库模型 (ORM)
"""
from sqlalchemy import Column, Integer, String, Float, Text
from app.database import Base


class Item(Base):
    """商品表"""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    tax = Column(Float, nullable=True)

    def __repr__(self):
        return f"<Item(id={self.id}, name='{self.name}', price={self.price})>"
