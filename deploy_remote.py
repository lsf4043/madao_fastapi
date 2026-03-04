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
SERVER_PASSWORD = "xiliu4043*."

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
        # 强制重置并拉取最新代码
        run_command(ssh, f"cd {PROJECT_DIR} && git fetch origin")
        run_command(ssh, f"cd {PROJECT_DIR} && git reset --hard origin/master")
        run_command(ssh, f"cd {PROJECT_DIR} && git pull origin master")

    # 安装依赖
    print("\n[5/7] 安装项目依赖...")
    print("-" * 30)

    run_command(ssh, f"cd {PROJECT_DIR} && pip3 install -r requirements.txt")

    # 初始化数据库
    print("\n[6/7] 初始化数据库...")
    print("-" * 30)

    run_command(ssh, f"cd {PROJECT_DIR} && python3 init_db.py")

    # 停止旧服务并启动新服务
    print("\n[7/7] 启动服务...")
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
    print("\n验证服务状态...")
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
