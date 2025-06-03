from datetime import datetime, timedelta

from db.crud import get_latest_post
from db.database import SessionLocal
from tasks.ptt_crawl import PttCrawler

db = SessionLocal()
latest_post = get_latest_post(db, 1)
crawler = PttCrawler(db, board="home-sale", board_id=1, cutoff_date=datetime.now() - timedelta(days=5))
posts = crawler.crawl()
post_finish = crawler.save_posts_from_postcrawls(posts)