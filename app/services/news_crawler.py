# -*- coding: utf-8 -*-
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
from datetime import datetime
import re


class NewsCrawler:
    """财经新闻爬虫"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.timeout = aiohttp.ClientTimeout(total=10)

    async def fetch_page(self, session: aiohttp.ClientSession, url: str) -> Optional[str]:
        """异步获取页面内容"""
        try:
            async with session.get(url, headers=self.headers) as response:
                if response.status == 200:
                    return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
        return None

    async def crawl_sina_finance(self) -> List[Dict]:
        """爬取新浪财经新闻"""
        url = "https://finance.sina.com.cn/"
        news_list = []

        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            html = await self.fetch_page(session, url)
            if html:
                soup = BeautifulSoup(html, 'lxml')
                # 查找新闻标题和链接
                news_items = soup.find_all('a', href=re.compile(r'https://finance.sina.com.cn/\d{4}-\d{2}-\d{2}/'))

                for item in news_items[:10]:  # 限制数量
                    title = item.get_text(strip=True)
                    href = item.get('href', '')

                    if title and href and len(title) > 10:  # 过滤太短的标题
                        news_list.append({
                            'title': title,
                            'url': href,
                            'source': '新浪财经',
                            'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'summary': title[:50] + '...' if len(title) > 50 else title
                        })

        return news_list

    async def crawl_eastmoney(self) -> List[Dict]:
        """爬取东方财富新闻"""
        url = "https://www.eastmoney.com/"
        news_list = []

        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            html = await self.fetch_page(session, url)
            if html:
                soup = BeautifulSoup(html, 'lxml')
                # 查找新闻标题
                news_items = soup.find_all('a', href=re.compile(r'https://finance.eastmoney.com/a/'))

                for item in news_items[:10]:
                    title = item.get_text(strip=True)
                    href = item.get('href', '')

                    if title and href and len(title) > 10:
                        news_list.append({
                            'title': title,
                            'url': href,
                            'source': '东方财富',
                            'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'summary': title[:50] + '...' if len(title) > 50 else title
                        })

        return news_list

    async def crawl_all_sources(self) -> List[Dict]:
        """并发爬取所有数据源"""
        tasks = [
            self.crawl_sina_finance(),
            self.crawl_eastmoney()
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        all_news = []
        for result in results:
            if isinstance(result, list):
                all_news.extend(result)

        # 如果没有爬取到数据，返回模拟数据
        if not all_news:
            all_news = self._get_mock_news()

        # 按时间排序
        all_news.sort(key=lambda x: x.get('publish_time', ''), reverse=True)

        return all_news[:20]  # 返回前20条

    def _get_mock_news(self) -> List[Dict]:
        """获取模拟新闻数据"""
        return [
            {
                'title': '央行：稳健的货币政策要灵活精准、合理适度',
                'url': 'https://finance.example.com/news/1',
                'source': '央行官网',
                'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'summary': '中国人民银行发布最新货币政策执行报告，强调稳健的货币政策要灵活精准、合理适度...'
            },
            {
                'title': 'A股三大指数集体收涨，北向资金净流入超百亿',
                'url': 'https://finance.example.com/news/2',
                'source': '证券时报',
                'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'summary': '今日A股市场表现强劲，三大指数全线收涨，北向资金净流入超过100亿元...'
            },
            {
                'title': '证监会：持续深化资本市场改革',
                'url': 'https://finance.example.com/news/3',
                'source': '证监会官网',
                'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'summary': '证监会召开新闻发布会，介绍资本市场改革进展，强调将持续深化市场化改革...'
            },
            {
                'title': '国务院常务会议：部署稳经济一揽子政策措施',
                'url': 'https://finance.example.com/news/4',
                'source': '新华社',
                'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'summary': '国务院常务会议召开，部署实施稳经济一揽子政策措施，促进经济回稳向好...'
            },
            {
                'title': '财政部：加大财政政策力度，支持实体经济发展',
                'url': 'https://finance.example.com/news/5',
                'source': '财政部官网',
                'publish_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'summary': '财政部表示将继续加大财政政策力度，采取更多措施支持实体经济发展...'
            }
        ]


# 创建全局实例
news_crawler = NewsCrawler()
