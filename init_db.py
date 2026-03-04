# -*- coding: utf-8 -*-
"""
数据库初始化脚本
创建所有表并添加默认管理员用户
"""
from app.database import engine, Base, SessionLocal
from app.models import User
from app.core.security import get_password_hash

# 创建所有表
Base.metadata.create_all(bind=engine)

# 创建默认管理员用户
db = SessionLocal()
try:
    # 检查是否已存在管理员
    admin = db.query(User).filter(User.username == "admin").first()
    if not admin:
        admin_user = User(
            username="admin",
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_superuser=True,
            is_active=True
        )
        db.add(admin_user)
        db.commit()
        print("默认管理员用户创建成功")
        print("用户名: admin")
        print("密码: admin123")
    else:
        print("管理员用户已存在")
finally:
    db.close()

print("数据库初始化完成")
