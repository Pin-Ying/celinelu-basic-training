# tasks/celery_tasks.py
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
import logging
import os

from db.database import SessionLocal
from db.crud import log_crawl_result, get_newest_post, get_all_boards, create_posts_bulk
from tasks.ptt_datacrawl import PttCrawler

load_dotenv()
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")

logger = logging.getLogger("ptt_crawler")
celery_app = Celery("ptt", broker=CELERY_BROKER_URL)

celery_app.conf.update(
    timezone='Asia/Taipei',
    enable_utc=False,
    beat_schedule={
        'crawl-ptt-every-hour': {
            'task': 'crawl_all_boards',
            'schedule': crontab(minute=0, hour='*/1'),
        },
    }
)


@celery_app.task(name="crawl_single_board_task")
def crawl_single_board_task(board: str, board_id: int):
    db = SessionLocal()
    try:
        newest_post = get_newest_post(db, board_id)
        if not newest_post:
            crawler = PttCrawler(db, board, board_id)
        else:
            crawler = PttCrawler(db, board, board_id, newest_post.created_at)
        log_crawl_result(db, f"[Crawl({board})]: Started!")

        posts = crawler.crawl()

        log_crawl_result(db, f"[Crawl({board})]: Finish! Crawled {len(posts)} posts")
        for i in range(0, len(posts), 50):
            log_crawl_result(db, f"[DB Save({board})]: Started! ({i} ~ {i + 50})")
            save_posts_to_db.delay(posts[i:i + 50])
            log_crawl_result(db, f"[DB Save({board})]: Finish! ({i} ~ {i + 50})")
    except Exception as e:
        log_crawl_result(db, f"[Crawl({board})]: Error! {e}", "ERROR")
        logger.error(f"[Crawl({board})]:Error! {e}")
    finally:
        db.close()


@celery_app.task(name="crawl_all_boards")
def crawl_all_boards():
    db = SessionLocal()
    ALL_BOARDS = get_all_boards(db)
    db.close()
    try:
        log_crawl_result(db, f"Task Started!")
        for board, board_id in ALL_BOARDS.items():
            crawl_single_board_task.delay(board, board_id)
        log_crawl_result(db, f"Task Finish!")
    except Exception as e:
        logger.error(f"[Crawl Error]: {e}", "ERROR")


@celery_app.task(name="save_posts_to_db", bind=True, max_retries=3, default_retry_delay=10)
def save_posts_to_db(self, board, post_inputs):
    db = SessionLocal()
    try:
        create_posts_bulk(db, post_inputs)
    except Exception as e:
        log_crawl_result(db, f"[DB Save({board})]: Error {e}", "ERROR")
        logger.error(f"[DB Save Error]: {e}")
        self.retry(exc=e)
    finally:
        db.close()
