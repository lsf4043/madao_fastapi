# -*- coding: utf-8 -*-
import paramiko
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SERVER_IP = "101.200.137.199"
SERVER_PORT = 22
SERVER_USER = "root"
SERVER_PASSWORD = "xiliu4043*."

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASSWORD)

def run_command(cmd):
    """执行命令"""
    stdin, stdout, stderr = ssh.exec_command(cmd)
    output = stdout.read().decode('utf-8')
    error = stderr.read().decode('utf-8')
    if output:
        print(output)
    if error:
        print(f"[ERROR] {error}")
    return output, error

print("=" * 50)
print("开始安装PostgreSQL")
print("=" * 50)

# 1. 安装PostgreSQL
print("\n[1/6] 安装PostgreSQL...")
run_command("yum install -y postgresql-server postgresql-contrib")

# 2. 初始化数据库
print("\n[2/6] 初始化数据库...")
run_command("postgresql-setup initdb")

# 3. 启动PostgreSQL服务
print("\n[3/6] 启动PostgreSQL服务...")
run_command("systemctl start postgresql")
run_command("systemctl enable postgresql")

# 4. 检查服务状态
print("\n[4/6] 检查服务状态...")
run_command("systemctl status postgresql")

# 5. 创建用户和数据库
print("\n[5/6] 创建用户和数据库...")
commands = [
    "sudo -u postgres psql -c \"CREATE USER lsf123456 WITH PASSWORD '123456';\"",
    "sudo -u postgres psql -c \"CREATE DATABASE finance_news OWNER lsf123456;\"",
    "sudo -u postgres psql -c \"GRANT ALL PRIVILEGES ON DATABASE finance_news TO lsf123456;\""
]
for cmd in commands:
    run_command(cmd)

# 6. 配置远程访问
print("\n[6/6] 配置远程访问...")
# 修改pg_hba.conf
run_command("echo 'host    all             all             0.0.0.0/0               md5' >> /var/lib/pgsql/data/pg_hba.conf")

# 修改postgresql.conf
run_command("sed -i \"s/#listen_addresses = 'localhost'/listen_addresses = '*'/\" /var/lib/pgsql/data/postgresql.conf")

# 重启PostgreSQL
run_command("systemctl restart postgresql")

print("\n" + "=" * 50)
print("PostgreSQL安装完成!")
print("=" * 50)
print("数据库: finance_news")
print("用户名: lsf123456")
print("密码: 123456")
print("端口: 5432")
print("=" * 50)

ssh.close()
