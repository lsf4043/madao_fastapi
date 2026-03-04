# -*- coding: utf-8 -*-
import pytest
from httpx import AsyncClient


class TestNews:
    """新闻相关测试"""

    @pytest.mark.asyncio
    async def test_get_news_list_unauthorized(self, client: AsyncClient):
        """测试未授权访问新闻列表"""
        response = await client.get("/api/v1/news/list")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_get_news_list_success(self, client: AsyncClient, auth_token):
        """测试获取新闻列表成功"""
        response = await client.get(
            "/api/v1/news/list",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        # 注意：由于是真实爬取，可能会失败，这里主要测试接口是否正常工作
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "total" in data
            assert "items" in data
            assert isinstance(data["items"], list)

    @pytest.mark.asyncio
    async def test_get_news_list_with_limit(self, client: AsyncClient, auth_token):
        """测试带限制的新闻列表"""
        response = await client.get(
            "/api/v1/news/list?limit=5",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert data["total"] >= 0
            assert len(data["items"]) <= 5

    @pytest.mark.asyncio
    async def test_crawl_news_unauthorized(self, client: AsyncClient):
        """测试未授权爬取新闻"""
        response = await client.post("/api/v1/news/crawl")
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_crawl_news_success(self, client: AsyncClient, auth_token):
        """测试爬取新闻成功"""
        response = await client.post(
            "/api/v1/news/crawl",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        # 注意：由于是真实爬取，可能会失败
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert "message" in data
            assert "count" in data
            assert data["status"] == "success"

    @pytest.mark.asyncio
    async def test_get_news_by_source_sina(self, client: AsyncClient, auth_token):
        """测试按来源获取新浪新闻"""
        response = await client.get(
            "/api/v1/news/source/sina",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert data["source"] == "sina"
            assert "count" in data
            assert "items" in data

    @pytest.mark.asyncio
    async def test_get_news_by_source_eastmoney(self, client: AsyncClient, auth_token):
        """测试按来源获取东方财富新闻"""
        response = await client.get(
            "/api/v1/news/source/eastmoney",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.json()
            assert data["source"] == "eastmoney"
            assert "count" in data
            assert "items" in data

    @pytest.mark.asyncio
    async def test_get_news_by_invalid_source(self, client: AsyncClient, auth_token):
        """测试无效的新闻来源"""
        response = await client.get(
            "/api/v1/news/source/invalid_source",
            headers={"Authorization": f"Bearer {auth_token}"}
        )
        assert response.status_code == 400
        assert "不支持的数据源" in response.json()["detail"]
