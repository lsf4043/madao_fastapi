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

print("=== 查看应用日志 ===")
stdin, stdout, stderr = ssh.exec_command("tail -50 /root/madao_fastapi/app.log")
print(stdout.read().decode('utf-8'))

print("\n=== 进程状态 ===")
stdin, stdout, stderr = ssh.exec_command("ps aux | grep uvicorn | grep -v grep")
print(stdout.read().decode('utf-8'))

print("\n=== 端口监听 ===")
stdin, stdout, stderr = ssh.exec_command("ss -tlnp | grep 8000")
print(stdout.read().decode('utf-8'))

ssh.close()
