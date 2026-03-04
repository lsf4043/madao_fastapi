# -*- coding: utf-8 -*-
import pytest
from httpx import AsyncClient


class TestHealth:
    """健康检查测试"""

    @pytest.mark.asyncio
    async def test_health_check(self, client: AsyncClient):
        """测试健康检查接口"""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "message" in data

    @pytest.mark.asyncio
    async def test_root_page(self, client: AsyncClient):
        """测试根路径"""
        response = await client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
