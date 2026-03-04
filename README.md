# 财经新闻爬取系统

基于 FastAPI 开发的财经新闻爬取系统，提供用户认证和新闻爬取功能。

## 功能特性

- 用户注册和登录
- JWT Token 认证
- 财经新闻爬取（开发中）
- 响应式前端界面

## 技术栈

- **后端**: FastAPI + SQLAlchemy + SQLite
- **前端**: HTML + CSS + JavaScript
- **认证**: JWT Token

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化数据库

```bash
python init_db.py
```

### 3. 启动服务

```bash
uvicorn app.main:app --reload
```

### 4. 访问应用

打开浏览器访问: http://localhost:8000

默认管理员账号:
- 用户名: admin
- 密码: admin123

## API 文档

启动服务后访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 项目结构

```
madao/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── database.py          # 数据库配置
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py        # 配置管理
│   │   └── security.py      # 安全相关功能
│   ├── models/
│   │   └── __init__.py      # 数据库模型
│   ├── schemas/
│   │   └── __init__.py      # Pydantic 模型
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py       # API 路由
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── auth.py  # 认证相关接口
│   │           └── news.py  # 新闻相关接口
│   └── static/
│       ├── login.html       # 登录页面
│       └── dashboard.html   # 控制台页面
├── init_db.py               # 数据库初始化脚本
├── requirements.txt         # 项目依赖
└── README.md               # 项目说明
```

## 开发计划

- [ ] 实现真实的新闻爬取功能
- [ ] 添加新闻分类和搜索
- [ ] 支持多数据源爬取
- [ ] 添加定时爬取任务
- [ ] 实现新闻收藏功能

## License

MIT
