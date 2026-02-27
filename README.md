# Madao FastAPI Test Project

这是一个FastAPI测试项目，包含基本的CRUD操作和完整的单元测试。

## 项目结构

```
madao/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI应用主文件
├── tests/
│   ├── __init__.py
│   └── test_main.py     # 单元测试文件
└── requirements.txt     # 项目依赖
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
uvicorn app.main:app --reload
```

访问 http://127.0.0.1:8000/docs 查看API文档

## 运行测试

```bash
pytest tests/ -v
```

## API端点

- `GET /` - 欢迎消息
- `POST /items/` - 创建新项目
- `GET /items/{item_id}` - 获取指定项目
- `PUT /items/{item_id}` - 更新指定项目
- `DELETE /items/{item_id}` - 删除指定项目
- `GET /items/` - 列出所有项目
