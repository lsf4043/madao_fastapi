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

# 测试验证
print("=== 测试验证 ===")
stdin, stdout, stderr = ssh.exec_command("""
cd /root/madao_fastapi
python3 -c "from app.schemas import UserCreate; u = UserCreate(username='ab', password='123'); print(u)"
""")
print(stdout.read().decode('utf-8'))
print(stderr.read().decode('utf-8'))

ssh.close()
