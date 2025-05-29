import logging
import os

from celery import Celery, chain, group
from celery.schedules import crontab
from dotenv import load_dotenv

from db.crud import log_crawl_result, get_newest_post, get_all_boards, create_posts_bulk
from db.database import SessionLocal
from schema.ptt_content import PostCrawl
from tasks.ptt_crawl import PttCrawler

load_dotenv()
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_BACKEND_URL = os.getenv("CELERY_BACKEND_URL")

logger = logging.getLogger("ptt_crawler")
celery_app = Celery("ptt", broker=CELERY_BROKER_URL, backend=CELERY_BACKEND_URL)

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
        if newest_post:
            crawler = PttCrawler(db, board, board_id, newest_post.created_at)
        else:
            crawler = PttCrawler(db, board, board_id)

        log_crawl_result(db, f"[Crawl({board})]: Started!")
        posts = crawler.crawl()
        post_dicts = [post.dict() for post in posts]
        log_crawl_result(db, f"[Crawl({board})]: Finish! Crawled {len(posts)} posts")

        # 回傳一組任務：先存 DB，再寫入 log
        save_tasks = [
            save_posts_to_db.s(board, post_dicts[i:i + 50])
            for i in range(0, len(posts), 50)
        ]
        return chain(
            group(save_tasks),
            all_sub_tasks_finished.s(f"[DB Save({board})]: Finish!")
        )()
    except Exception as e:
        log_crawl_result(db, f"[Crawl({board})]: Error! {e}", "ERROR")
        logger.error(f"[Crawl({board})]: Error! {e}")
    finally:
        db.close()


@celery_app.task(name="crawl_all_boards")
def crawl_all_boards():
    db = SessionLocal()
    log_crawl_result(db, f"Task Started!")
    ALL_BOARDS = get_all_boards(db)
    db.close()
    try:
        # 確定 crawl_single_board_task 都完成並傳訊息
        header_tasks = [
            crawl_single_board_task.s(board, board_id)
            for board, board_id in ALL_BOARDS.items()
        ]
        chain(
            group(header_tasks),
            all_sub_tasks_finished.s(f"Task Finished!")
        )()

    except Exception as e:
        logger.error(f"[Crawl Error]: {e}", "ERROR")


@celery_app.task(name="save_posts_to_db", bind=True, max_retries=3, default_retry_delay=10)
def save_posts_to_db(self, board, post_dicts: dict):
    db = SessionLocal()
    try:
        post_inputs = [PostCrawl(**post) for post in post_dicts]
        create_posts_bulk(db, post_inputs)
    except Exception as e:
        # 如果還沒到最大重試次數，重試但不紀錄錯誤
        if self.request.retries < self.max_retries:
            log_crawl_result(db, f"[DB Saving({board})]: Retrying! {e}", "WARNING")
            raise self.retry(exc=e)
        # 如果已經是最後一次重試失敗，才記錄錯誤
        log_crawl_result(db, f"[DB Saving({board})]: Retry Failed {e}", "ERROR")
        logger.error(f"[DB Saving({board})]: Retry Failed {e}")
    finally:
        db.close()


@celery_app.task
def all_sub_tasks_finished(msg="Task Finish!"):
    db = SessionLocal()
    try:
        log_crawl_result(db, msg)
        return msg
    finally:
        db.close()
