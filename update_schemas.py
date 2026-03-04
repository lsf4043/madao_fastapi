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

# 直接上传更新后的schemas文件
schemas_content = '''# -*- coding: utf-8 -*-
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=20, description="用户名长度3-20个字符")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")


class UserCreate(UserBase):
    """用户创建模型"""
    password: str = Field(..., min_length=6, max_length=50, description="密码长度6-50个字符")

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        """验证用户名"""
        if not v:
            raise ValueError('用户名不能为空')
        if not v.isalnum():
            raise ValueError('用户名只能包含字母和数字')
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """验证密码"""
        if not v:
            raise ValueError('密码不能为空')
        if len(v) < 6:
            raise ValueError('密码长度至少6个字符')
        return v


class UserLogin(BaseModel):
    """用户登录模型"""
    username: str
    password: str


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """令牌模型"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """令牌数据"""
    username: Optional[str] = None
'''

# 使用SFTP上传文件
sftp = ssh.open_sftp()
with sftp.file('/root/madao_fastapi/app/schemas/__init__.py', 'w') as f:
    f.write(schemas_content)
sftp.close()

print("schemas文件已更新")

# 重启服务
stdin, stdout, stderr = ssh.exec_command("pkill -f 'uvicorn app.main:app' 2>/dev/null || true")
stdout.read()

stdin, stdout, stderr = ssh.exec_command("""
cd /root/madao_fastapi
nohup python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /root/madao_fastapi/app.log 2>&1 &
sleep 3
echo "服务已重启"
""")
print(stdout.read().decode('utf-8'))

ssh.close()
