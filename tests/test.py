from datetime import datetime

from db.crud import get_latest_post, create_log_result
from db.database import SessionLocal
from tasks.ptt_crawl import PttCrawler

db = SessionLocal()
try:
    latest_post = get_latest_post(db, 1)

    # 爬取
    crawler = PttCrawler(db, "home-sale", 1)
    crawler.cutoff_date = datetime(2025,6,9)
    posts = crawler.crawl_all_articles()

    # 存入
    post_finish, post_exception_msgs = crawler.save_posts_from_postcrawls(posts)
    if len(post_exception_msgs) > 0:
        for msg in post_exception_msgs:
            print(msg)
    print(f"saved {len(post_finish)} posts")
except Exception as e:
    print(e)
    raise e
finally:
    db.close()
