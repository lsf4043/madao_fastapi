# -*- coding: utf-8 -*-
"""
数据库初始化脚本
创建所有表并添加默认管理员用户
"""
import asyncio
from app.database import engine, Base, AsyncSessionLocal
from app.models import User
from app.core.security import get_password_hash
from sqlalchemy import select


async def init_database():
    """初始化数据库"""
    # 创建所有表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 创建默认管理员用户
    async with AsyncSessionLocal() as db:
        try:
            # 检查是否已存在管理员
            result = await db.execute(select(User).where(User.username == "admin"))
            admin = result.scalar_one_or_none()

            if not admin:
                admin_user = User(
                    username="admin",
                    email="admin@example.com",
                    hashed_password=get_password_hash("admin123"),
                    is_superuser=True,
                    is_active=True
                )
                db.add(admin_user)
                await db.commit()
                print("默认管理员用户创建成功")
                print("用户名: admin")
                print("密码: admin123")
            else:
                print("管理员用户已存在")
        except Exception as e:
            await db.rollback()
            print(f"创建管理员用户失败: {e}")
            raise

    print("数据库初始化完成")


if __name__ == "__main__":
    asyncio.run(init_database())
