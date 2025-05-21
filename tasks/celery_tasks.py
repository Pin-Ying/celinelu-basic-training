# tasks/celery_tasks.py
from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv
import logging
import os

from db.crud import log_crawl_result, get_newest_post
from schema.ptt_content import PostInput
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

ALL_BOARDS = {'Stock': 1, 'Baseball': 2, 'NBA': 3, 'HatePolitics': 4, 'Lifeismoney': 5}


@celery_app.task(name="crawl_single_board_task")
def crawl_single_board_task(board: str, board_id: int):
    from db.database import SessionLocal
    from db.crud import log_crawl_result

    db = SessionLocal()
    try:
        newest_post = get_newest_post(db)
        if not newest_post:
            crawler = PttCrawler(db, board, board_id)
        else:
            crawler = PttCrawler(db, board, board_id, newest_post.created_at)
        log_crawl_result(db, f"{board}:Crawling Start!")

        posts = crawler.crawl()
        post_dicts = [post.dict() for post in posts]

        log_crawl_result(db, f"{board}:Finish! Crawled {len(posts)} posts")
        save_posts_to_db.delay(post_dicts)
    except Exception as e:
        log_crawl_result(db, f"{board}:Error! {e}", "ERROR")
        logger.error(f"[{board} Crawl Error]: {e}")
    finally:
        db.close()


@celery_app.task(name="crawl_all_boards")
def crawl_all_boards():
    try:
        for board, board_id in ALL_BOARDS.items():
            crawl_single_board_task.delay(board, board_id)
    except Exception as e:
        logger.error(f"[Crawl Error]: {e}", "ERROR")


@celery_app.task(name="save_posts_to_db", bind=True, max_retries=3, default_retry_delay=10)
def save_posts_to_db(self, post_dicts):
    from db.database import SessionLocal
    from db.crud import create_posts_bulk

    db = SessionLocal()
    try:
        post_inputs = [PostInput(**post) for post in post_dicts]
        create_posts_bulk(db, post_inputs)
    except Exception as e:
        log_crawl_result(db, f"[DB Save Error]: {e}", "ERROR")
        logger.error(f"[DB Save Error]: {e}")
        self.retry(exc=e)
    finally:
        db.close()
