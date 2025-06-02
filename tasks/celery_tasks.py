import logging
import os

from celery import Celery, chain, group
from celery.schedules import crontab
from dotenv import load_dotenv

from db.crud import log_crawl_result, get_latest_post, get_all_boards, create_posts
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
        latest_post = get_latest_post(db, board_id)
        crawler = PttCrawler(db, board, board_id, latest_post.created_at if latest_post else None)

        posts = crawler.crawl()
        post_dicts = [post.modul_dump() for post in posts]
        return {"board": board, "posts": post_dicts}
    except Exception as e:
        log_crawl_result(db, f"[Crawl({board})]: Error! {e}", "ERROR")
        logger.error(f"[Crawl({board})]: Error! {e}")
    finally:
        db.close()


@celery_app.task(name="split_and_save_posts")
def split_and_save_posts(crawl_result: dict):
    board = crawl_result["board"]
    post_dicts = crawl_result["posts"]

    task_group = group([
        save_posts_to_db.s(board, post_dicts[i:i + 50])
        for i in range(0, len(post_dicts), 50)
    ])
    task_group.apply_async()
    return f"[DB Saving({board})]: Started."


@celery_app.task(name="save_posts_to_db", bind=True, max_retries=3, default_retry_delay=10)
def save_posts_to_db(self, board, post_dicts: dict):
    db = SessionLocal()
    try:
        post_inputs = [PostCrawl(**post) for post in post_dicts]
        for input in post_inputs:
            pass # ToDo



        create_posts(db, post_inputs)
    except Exception as e:
        if self.request.retries < self.max_retries:
            log_crawl_result(db, f"[DB Saving({board})]: Retrying! {e}", "WARNING")
            raise self.retry(exc=e)
        log_crawl_result(db, f"[DB Saving({board})]: Retry Failed. {e}", "ERROR")
        logger.error(f"[DB Saving({board})]: Retry Failed {e}")
    finally:
        db.close()


@celery_app.task
def tasks_log(result, msg="Task Finish!"):
    db = SessionLocal()
    try:
        log_crawl_result(db, msg)
        return msg
    finally:
        db.close()


@celery_app.task(name="crawl_all_boards")
def crawl_all_boards():
    db = SessionLocal()
    log_crawl_result(db, f"Task Started!")
    ALL_BOARDS = get_all_boards(db)
    db.close()

    try:
        # 為每個 board 建立 chain: 爬文 → 分段存資料 → 紀錄完成
        full_tasks = []
        for board, board_id in ALL_BOARDS.items():
            full_chain = chain(
                crawl_single_board_task.s(board, board_id),
                split_and_save_posts.s(),
                tasks_log.s(f"[{board}] Finished.")
            )
            full_tasks.append(full_chain)

        # 用 group 包起所有 board 的完整任務
        chain(
            group(full_tasks),
            tasks_log.s("All Boards Finished! Task Finish.")
        ).apply_async()
    except Exception as e:
        log_crawl_result(db, f"Error： {e}", "ERROR")
        logger.error(f"Error： {e}", "ERROR")
