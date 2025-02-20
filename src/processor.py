from datetime import datetime
from typing import List, Dict, Any

class NewsProcessor:
    def __init__(self):
        self.categories = {
            'cloud_services': ['阿里云', '腾讯云', '华为云', 'AWS', 'Oracle Cloud'],
            'database_products': ['MySQL', 'PostgreSQL', 'Oracle', 'MongoDB', 'Redis', 'OceanBase'],
            'technology': ['性能优化', '高可用', '分布式', '架构设计', '最佳实践'],
            'industry': ['数据库行业', '技术趋势', '案例分析']
        }

    def categorize_news(self, news_item: Dict[str, Any]) -> List[str]:
        categories = []
        title = news_item['title'].lower()
        
        for category, keywords in self.categories.items():
            for keyword in keywords:
                if keyword.lower() in title:
                    categories.append(category)
                    break
        
        return categories if categories else ['other']

    def format_daily_report(self, news_items: List[Dict[str, Any]]) -> str:
        if not news_items:
            return "今日暂无数据库相关新闻。"

        # Sort news by category
        categorized_news = {}
        for item in news_items:
            categories = self.categorize_news(item)
            for category in categories:
                if category not in categorized_news:
                    categorized_news[category] = []
                categorized_news[category].append(item)

        # Format the report
        report = [
            f"数据库资讯日报 - {datetime.now().strftime('%Y/%m/%d')}\n",
            "本资讯由数据库资讯智能助手生成\n",
            "\n== 内容总结 ==\n"
        ]

        # Add summary
        total_news = len(news_items)
        report.append(f"今日共收集到 {total_news} 条数据库相关资讯，")
        report.append(f"涉及 {len(categorized_news)} 个主要领域。\n")

        # Add detailed content
        report.append("\n== 详细内容 ==\n")
        
        for category, items in categorized_news.items():
            category_name = category.replace('_', ' ').title()
            report.append(f"\n{category_name}:")
            
            for item in items:
                report.append(f"\n- {item['title']}")
                report.append(f"  来源: {item['source']}")
                report.append(f"  链接: {item['url']}")
                report.append(f"  日期: {item['date']}\n")

        # Add sources summary
        report.append("\n== 信息来源 ==\n")
        sources = set(item['source'] for item in news_items)
        for source in sources:
            report.append(f"- {source}")

        return "\n".join(report)

    def generate_html_report(self, news_items: List[Dict[str, Any]]) -> str:
        if not news_items:
            return "<h1>今日暂无数据库相关新闻。</h1>"

        categorized_news = {}
        for item in news_items:
            categories = self.categorize_news(item)
            for category in categories:
                if category not in categorized_news:
                    categorized_news[category] = []
                categorized_news[category].append(item)

        html = f"""
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; margin-top: 20px; }}
                .summary {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
                .news-item {{ margin: 10px 0; padding: 10px; border-left: 3px solid #007bff; }}
                .source {{ color: #666; font-size: 0.9em; }}
                .date {{ color: #999; font-size: 0.8em; }}
            </style>
        </head>
        <body>
            <h1>数据库资讯日报 - {datetime.now().strftime('%Y/%m/%d')}</h1>
            <p>本资讯由数据库资讯智能助手生成</p>
            
            <h2>内容总结</h2>
            <div class="summary">
                <p>今日共收集到 {len(news_items)} 条数据库相关资讯，涉及 {len(categorized_news)} 个主要领域。</p>
            </div>
            
            <h2>详细内容</h2>
        """

        for category, items in categorized_news.items():
            category_name = category.replace('_', ' ').title()
            html += f"<h3>{category_name}</h3>"
            
            for item in items:
                html += f"""
                <div class="news-item">
                    <h4><a href="{item['url']}">{item['title']}</a></h4>
                    <p class="source">来源: {item['source']}</p>
                    <p class="date">日期: {item['date']}</p>
                </div>
                """

        html += """
            <h2>信息来源</h2>
            <ul>
        """
        
        sources = set(item['source'] for item in news_items)
        for source in sources:
            html += f"<li>{source}</li>"

        html += """
            </ul>
        </body>
        </html>
        """

        return html
