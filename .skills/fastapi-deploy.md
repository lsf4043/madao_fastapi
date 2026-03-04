# FastAPI 项目部署到阿里云服务器

## Skill 描述

将本地 FastAPI 项目自动部署到阿里云 ECS 服务器，包括：
- 连接远程服务器
- 检查并安装服务器环境（Git、Python 依赖）
- 克隆/更新代码
- 启动服务
- 配置安全组端口
- 验证服务运行状态

---

## 配置信息

### GitHub 配置

| 配置项 | 值 |
|--------|-----|
| GitHub 用户名 | `lsf4043` |
| 仓库地址 | `https://github.com/lsf4043/madao_fastapi.git` |
| SSH 地址 | `git@github.com:lsf4043/madao_fastapi.git` |
| GitHub Token | `<YOUR_GITHUB_TOKEN>` |

### 阿里云服务器配置

| 配置项 | 值 |
|--------|-----|
| 服务器 IP | `101.200.137.199` |
| SSH 端口 | `22` |
| 用户名 | `root` |
| 密码 | `<YOUR_SERVER_PASSWORD>` |
| 项目目录 | `/root/madao_fastapi` |
| 服务端口 | `8000` |

---

## 前置条件

1. 本地已安装 Python 和 paramiko 模块
2. 有阿里云 ECS 服务器访问权限
3. 项目代码已上传到 GitHub 仓库
4. 阿里云安全组已配置（或需要配置）

---

## 部署流程

### 1. 安装 paramiko 模块

```bash
pip install paramiko
```

### 2. 创建部署脚本

创建 `deploy_remote.py` 文件：

```python
# -*- coding: utf-8 -*-
import paramiko
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 服务器配置
SERVER_IP = "101.200.137.199"
SERVER_PORT = 22
SERVER_USER = "root"
SERVER_PASSWORD = "<YOUR_SERVER_PASSWORD>"

# GitHub 仓库地址
REPO_URL = "https://github.com/lsf4043/madao_fastapi.git"
PROJECT_DIR = "/root/madao_fastapi"

def run_command(ssh, command, show_output=True):
    """执行远程命令"""
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')

    if show_output:
        if output:
            print(output)
        if error and "WARNING" not in error:
            print(f"[ERROR] {error}")

    return output, error

def main():
    print("=" * 50)
    print("开始部署 FastAPI 项目到阿里云服务器")
    print("=" * 50)

    # 连接服务器
    print("\n[1/7] 连接服务器...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)
        print(f"[OK] 成功连接到 {SERVER_IP}")
    except Exception as e:
        print(f"[FAIL] 连接失败: {e}")
        return

    # 检查服务器环境
    print("\n[2/7] 检查服务器环境...")
    print("-" * 30)

    run_command(ssh, "echo '=== 系统信息 ===' && uname -a")
    run_command(ssh, "echo '=== Python 版本 ===' && python3 --version")

    # 检查 Git 是否安装
    print("\n[3/7] 检查并安装 Git...")
    print("-" * 30)

    stdin, stdout, stderr = ssh.exec_command("which git")
    stdout.read()
    exit_status = stdout.channel.recv_exit_status()

    if exit_status != 0:
        print("Git 未安装，正在安装...")
        run_command(ssh, "yum install -y git")
    else:
        print("Git 已安装")

    # 克隆或更新代码
    print("\n[4/7] 克隆/更新代码...")
    print("-" * 30)

    stdin, stdout, stderr = ssh.exec_command(f"test -d {PROJECT_DIR}")
    stdout.read()
    exit_status = stdout.channel.recv_exit_status()

    if exit_status != 0:
        print("项目目录不存在，正在克隆...")
        run_command(ssh, f"git clone {REPO_URL} {PROJECT_DIR}")
    else:
        print("项目目录已存在，正在更新...")
        run_command(ssh, f"cd {PROJECT_DIR} && git pull origin master")

    # 安装依赖
    print("\n[5/7] 安装项目依赖...")
    print("-" * 30)

    run_command(ssh, f"cd {PROJECT_DIR} && pip3 install -r requirements.txt")

    # 停止旧服务并启动新服务
    print("\n[6/7] 启动服务...")
    print("-" * 30)

    run_command(ssh, "pkill -f 'uvicorn app.main:app' 2>/dev/null || true")

    start_cmd = f"""
cd {PROJECT_DIR}
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > {PROJECT_DIR}/app.log 2>&1 &
sleep 3
echo "服务启动命令已执行"
"""
    run_command(ssh, start_cmd)

    # 验证服务状态
    print("\n[7/7] 验证服务状态...")
    print("-" * 30)

    run_command(ssh, "ps aux | grep uvicorn | grep -v grep || echo '未找到 uvicorn 进程'")
    run_command(ssh, "netstat -tlnp 2>/dev/null | grep 8000 || ss -tlnp 2>/dev/null | grep 8000 || echo '端口 8000 未监听'")

    time.sleep(2)
    run_command(ssh, "curl -s http://localhost:8000/ || echo 'API 测试失败'")

    ssh.close()

    print("\n" + "=" * 50)
    print("[OK] 部署完成!")
    print("=" * 50)
    print(f"服务地址: http://{SERVER_IP}:8000")
    print(f"API 文档: http://{SERVER_IP}:8000/docs")
    print("=" * 50)

if __name__ == "__main__":
    main()
```

### 3. 执行部署

```bash
python deploy_remote.py
```

---

## 阿里云安全组配置

如果外网无法访问，需要在阿里云控制台配置安全组：

### 配置步骤

1. 登录阿里云 ECS 控制台：https://ecs.console.aliyun.com/
2. 左侧菜单：**实例与镜像** → **实例**
3. 找到 IP 为 `101.200.137.199` 的实例，点击实例 ID
4. 点击 **安全组** 标签页
5. 点击安全组 ID 进入详情
6. 点击 **手动添加** 或 **快速添加**

### 入方向规则配置

| 配置项 | 值 |
|--------|-----|
| 授权策略 | 允许 |
| 优先级 | 1 |
| 协议类型 | 自定义 TCP |
| 端口范围 | 8000/8000 |
| 授权对象 | 0.0.0.0/0 |
| 描述 | FastAPI 服务 |

### 重要说明

- **入方向**：外部访问服务器（用户访问你的服务）→ 需要开放服务端口
- **出方向**：服务器访问外部（默认允许）→ 一般不用配置

---

## 验证部署

访问以下地址验证：
- 首页：http://101.200.137.199:8000
- API 文档：http://101.200.137.199:8000/docs

---

## 常用命令

### 检查服务状态脚本

```python
# check_service.py
import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SERVER_IP = "101.200.137.199"
SERVER_PORT = 22
SERVER_USER = "root"
SERVER_PASSWORD = "<YOUR_SERVER_PASSWORD>"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)

print("=== 进程状态 ===")
stdin, stdout, stderr = ssh.exec_command("ps aux | grep uvicorn | grep -v grep")
print(stdout.read().decode('utf-8'))

print("=== 端口监听 ===")
stdin, stdout, stderr = ssh.exec_command("ss -tlnp | grep 8000")
print(stdout.read().decode('utf-8'))

print("=== API 测试 ===")
stdin, stdout, stderr = ssh.exec_command("curl -s http://localhost:8000/")
print(stdout.read().decode('utf-8'))

ssh.close()
```

### 查看日志

```bash
tail -f /root/madao_fastapi/app.log
```

### 重启服务

```bash
pkill -f 'uvicorn app.main:app'
cd /root/madao_fastapi
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
```

### 停止服务

```bash
pkill -f 'uvicorn app.main:app'
```

---

## 注意事项

1. 服务器防火墙默认不阻止，但阿里云安全组需要手动配置
2. 入方向规则控制外部访问服务器，出方向规则控制服务器访问外部
3. 服务使用 nohup 后台运行，服务器重启后需要手动重启服务
4. 建议使用 systemd 或 supervisor 管理服务，实现开机自启

---

## 快速部署命令

下次只需要告诉我：**"按照 fastapi-deploy skill 部署"**，我就会自动执行以上流程。
