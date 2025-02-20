import logging
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timedelta
import yaml
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class DatabaseNewsCrawler:
    def __init__(self, config_path: str):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def fetch_page(self, url: str) -> str:
        try:
            async with self.session.get(url) as response:
                return await response.text()
        except Exception as e:
            logger.error(f"Error fetching {url}: {str(e)}")
            return ""

    async def parse_cloud_website(self, website: Dict[str, str]) -> List[Dict[str, Any]]:
        html = await self.fetch_page(website['url'])
        if not html:
            return []

        soup = BeautifulSoup(html, 'lxml')
        articles = []
        
        # This is a simplified version. You'll need to customize the selectors
        # based on each website's specific structure
        for article in soup.select('article, .news-item, .blog-post')[:5]:
            title = article.select_one('h2, .title')
            link = article.select_one('a')
            date = article.select_one('.date, .time')
            
            if title and link:
                articles.append({
                    'title': title.text.strip(),
                    'url': link.get('href', ''),
                    'date': date.text.strip() if date else datetime.now().strftime('%Y-%m-%d'),
                    'source': website['name']
                })

        return articles

    async def parse_rss_feed(self, blog: Dict[str, str]) -> List[Dict[str, Any]]:
        feed = feedparser.parse(blog['url'])
        articles = []

        for entry in feed.entries[:5]:
            articles.append({
                'title': entry.title,
                'url': entry.link,
                'date': datetime.fromtimestamp(
                    entry.get('published_parsed', entry.get('updated_parsed'))
                ).strftime('%Y-%m-%d'),
                'source': blog['name']
            })

        return articles

    async def collect_all_news(self) -> List[Dict[str, Any]]:
        all_news = []
        
        # Collect from cloud websites
        cloud_tasks = [
            self.parse_cloud_website(website)
            for website in self.config['sources']['cloud_websites']
        ]
        cloud_results = await asyncio.gather(*cloud_tasks)
        for result in cloud_results:
            all_news.extend(result)

        # Collect from expert blogs
        blog_tasks = [
            self.parse_rss_feed(blog) if blog['type'] == 'rss'
            else self.parse_cloud_website(blog)
            for blog in self.config['sources']['expert_blogs']
        ]
        blog_results = await asyncio.gather(*blog_tasks)
        for result in blog_results:
            all_news.extend(result)

        # Filter news from the last 24 hours
        cutoff_date = datetime.now() - timedelta(days=1)
        filtered_news = [
            news for news in all_news
            if datetime.strptime(news['date'], '%Y-%m-%d') >= cutoff_date
        ]

        return filtered_news

async def main():
    async with DatabaseNewsCrawler('config/config.yaml') as crawler:
        news = await crawler.collect_all_news()
        print(f"Collected {len(news)} news items")

if __name__ == '__main__':
    asyncio.run(main())
