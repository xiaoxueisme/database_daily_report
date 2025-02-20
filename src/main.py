import asyncio
import logging
import os
import yaml
import schedule
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from crawler import DatabaseNewsCrawler
from processor import NewsProcessor
from wechat_pusher import WeChatPusher

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/daily_report.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DatabaseDailyReport:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Load configuration
        config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = yaml.safe_load(f)

        # Initialize components
        self.crawler = DatabaseNewsCrawler(str(config_path))
        self.processor = NewsProcessor()
        
        # Use webhook URL from config or environment variable
        webhook_url = os.getenv('WECHAT_WEBHOOK_URL') or self.config['wechat']['webhook_url']
        self.wechat_pusher = WeChatPusher(webhook_url)

    async def generate_and_send_report(self):
        """Generate and send the daily report."""
        try:
            logger.info("Starting daily report generation")
            
            # Collect news
            async with self.crawler as crawler:
                news_items = await crawler.collect_all_news()
            
            if not news_items:
                logger.warning("No news items found today")
                return
            
            # Process news
            text_report = self.processor.format_daily_report(news_items)
            html_report = self.processor.generate_html_report(news_items)
            
            # Send report
            success = await self.wechat_pusher.send_daily_report(
                text_content=text_report,
                html_content=html_report
            )
            
            if success:
                logger.info("Daily report sent successfully")
            else:
                logger.error("Failed to send daily report")
                
        except Exception as e:
            logger.error(f"Error generating daily report: {str(e)}", exc_info=True)

def run_report():
    """Run the report generation process."""
    report = DatabaseDailyReport()
    asyncio.run(report.generate_and_send_report())

def main():
    """Main function to schedule and run the daily report."""
    logger.info("Starting Database Daily Report Service")
    
    # Schedule the report
    schedule_time = "10:00"  # Default time
    if 'report' in config and 'schedule_time' in config['report']:
        schedule_time = config['report']['schedule_time']
    
    schedule.every().day.at(schedule_time).do(run_report)
    logger.info(f"Scheduled daily report for {schedule_time}")
    
    # Run the report immediately if it's the first run of the day
    current_time = datetime.now()
    if current_time.hour < int(schedule_time.split(':')[0]):
        logger.info("Running initial report")
        run_report()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
