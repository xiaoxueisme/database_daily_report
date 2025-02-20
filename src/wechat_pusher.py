import json
import logging
from typing import Union
import aiohttp
from datetime import datetime

logger = logging.getLogger(__name__)

class WeChatPusher:
    def __init__(self, webhook_url: str):
        """Initialize with webhook URL instead of enterprise application credentials."""
        self.webhook_url = webhook_url

    async def send_message(self, content: Union[str, dict], msg_type: str = "text") -> bool:
        """Send message using webhook."""
        try:
            async with aiohttp.ClientSession() as session:
                if msg_type == "text":
                    message = {
                        "msgtype": "text",
                        "text": {
                            "content": content
                        }
                    }
                elif msg_type == "markdown":
                    message = {
                        "msgtype": "markdown",
                        "markdown": {
                            "content": content
                        }
                    }
                else:
                    raise ValueError(f"Unsupported message type: {msg_type}")

                async with session.post(self.webhook_url, json=message) as response:
                    result = await response.json()
                    if result.get("errcode") == 0:
                        logger.info("Message sent successfully")
                        return True
                    else:
                        logger.error(f"Failed to send message: {result}")
                        return False

        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return False

    async def send_daily_report(self, text_content: str, html_content: str) -> bool:
        """Send daily report using markdown format."""
        # Convert HTML to markdown-like format for WeChat
        markdown_content = self._html_to_markdown(html_content)
        return await self.send_message(markdown_content, "markdown")

    def _html_to_markdown(self, html_content: str) -> str:
        """Convert HTML content to WeChat markdown format."""
        markdown = []
        
        # Extract title
        title_start = html_content.find("<h1>") + 4
        title_end = html_content.find("</h1>")
        if title_start > 3 and title_end > 0:
            markdown.append(f"# {html_content[title_start:title_end].strip()}\n")

        # Extract summary
        summary_start = html_content.find('class="summary">')
        if summary_start > 0:
            summary_end = html_content.find("</div>", summary_start)
            summary = html_content[summary_start + 15:summary_end]
            summary = summary.replace("<p>", "").replace("</p>", "\n")
            markdown.append(f"\n## 内容总结\n{summary}\n")

        # Extract news items
        news_items = html_content.split('class="news-item"')[1:]
        markdown.append("\n## 详细内容\n")
        
        for item in news_items:
            # Extract title
            title_start = item.find("<h4>") + 4
            title_end = item.find("</h4>")
            if title_start > 3 and title_end > 0:
                title = item[title_start:title_end].strip()
                title = title.replace("<a href=\"", "").replace("</a>", "")
                url_end = title.find("\">")
                if url_end > 0:
                    url = title[:url_end]
                    title = title[url_end + 2:]
                    markdown.append(f"\n### [{title}]({url})")

            # Extract source and date
            source_start = item.find('class="source">') + 14
            source_end = item.find("</p>", source_start)
            if source_start > 13 and source_end > 0:
                markdown.append(item[source_start:source_end].strip())

            date_start = item.find('class="date">') + 12
            date_end = item.find("</p>", date_start)
            if date_start > 11 and date_end > 0:
                markdown.append(item[date_start:date_end].strip() + "\n")

        return "\n".join(markdown)
