# 部署指南

## 1. 上传到GitHub

### 1.1 初始化Git仓库
```bash
cd D:\madao
git init
git add .
git commit -m "Initial commit: FastAPI project with tests"
```

### 1.2 创建GitHub仓库并推送
1. 在GitHub上创建新仓库（例如：fastapi-madao）
2. 添加远程仓库并推送：
```bash
git remote add origin https://github.com/你的用户名/fastapi-madao.git
git branch -M main
git push -u origin main
```

## 2. 云服务器部署

### 方案一：使用Docker部署（推荐）

#### 2.1 在云服务器上安装Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 启动Docker服务
sudo systemctl start docker
sudo systemctl enable docker
```

#### 2.2 从GitHub克隆项目
```bash
git clone https://github.com/你的用户名/fastapi-madao.git
cd fastapi-madao
```

#### 2.3 使用Docker Compose部署
```bash
# 构建并启动服务
sudo docker-compose up -d

# 查看运行状态
sudo docker-compose ps

# 查看日志
sudo docker-compose logs -f
```

#### 2.4 更新部署
```bash
# 拉取最新代码
git pull origin main

# 重新构建并启动
sudo docker-compose up -d --build
```

### 方案二：直接部署（不使用Docker）

#### 2.1 安装Python环境
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip -y
```

#### 2.2 克隆项目并安装依赖
```bash
git clone https://github.com/你的用户名/fastapi-madao.git
cd fastapi-madao
pip3 install -r requirements.txt
```

#### 2.3 使用Gunicorn运行
```bash
# 安装Gunicorn
pip3 install gunicorn

# 启动服务
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

#### 2.4 使用Systemd管理服务
创建服务文件 `/etc/systemd/system/fastapi-madao.service`：
```ini
[Unit]
Description=FastAPI Madao Application
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/fastapi-madao
Environment="PATH=/path/to/fastapi-madao/venv/bin"
ExecStart=/path/to/fastapi-madao/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl start fastapi-madao
sudo systemctl enable fastapi-madao
```

## 3. Nginx反向代理配置

创建Nginx配置文件 `/etc/nginx/sites-available/fastapi-madao`：
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

启用配置：
```bash
sudo ln -s /etc/nginx/sites-available/fastapi-madao /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 4. 防火墙配置

```bash
# 开放必要端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp  # 如果不使用Nginx
sudo ufw enable
```

## 5. SSL证书配置（可选）

使用Let's Encrypt免费证书：
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## 6. 监控和日志

### 查看应用日志
```bash
# Docker方式
sudo docker-compose logs -f

# Systemd方式
sudo journalctl -u fastapi-madao -f
```

### 健康检查
访问 `http://your-domain.com/` 或 `http://your-domain.com/docs` 确认服务正常运行。

## 7. 常见问题

### 端口被占用
```bash
# 查看端口占用
sudo lsof -i :8000

# 结束占用进程
sudo kill -9 <PID>
```

### 权限问题
```bash
# 给予项目目录适当权限
sudo chown -R www-data:www-data /path/to/fastapi-madao
```

### Docker容器无法启动
```bash
# 查看详细错误信息
sudo docker-compose logs

# 重新构建
sudo docker-compose down
sudo docker-compose build --no-cache
sudo docker-compose up -d
```
