import logging
import os
from datetime import datetime

from celery import Celery, chain, group
from celery.schedules import crontab
from dotenv import load_dotenv

from db.crud import log_crawl_result, get_latest_post, get_all_boards
from db.database import SessionLocal
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
def crawl_single_board_task(task_id, board: str, board_id: int):
    db = SessionLocal()
    try:
        latest_post = get_latest_post(db, board_id)

        # 爬取
        crawler = PttCrawler(db, board, board_id, latest_post=latest_post) if latest_post else PttCrawler(db, board, board_id)
        posts = crawler.crawl_all_articles()

        # 存入
        post_finish = crawler.save_posts_from_postcrawls(posts)
        return f"saved {len(post_finish)} posts"
    except Exception as e:
        log_crawl_result(db,task_id, f"[{board}]: Error! {e}", "ERROR")
        logger.error(f"[{board}]: Error! {e}")
        raise e
    finally:
        db.close()


@celery_app.task
def tasks_log(result, task_id, msg="Task Finish!", show_result=False):
    db = SessionLocal()
    try:
        if result and show_result:
            msg += f"Result: {result}."
        log_crawl_result(db, task_id, msg)
        return msg
    finally:
        db.close()


@celery_app.task(name="crawl_all_boards")
def crawl_all_boards():
    db = SessionLocal()
    task_id = "task-" + datetime.now().strftime("%Y%m%d%H%M%S")
    log_crawl_result(db, task_id, f"Task Started!")
    all_boards = get_all_boards(db)

    try:
        full_tasks = []
        for board, board_id in all_boards.items():
            full_chain = chain(
                crawl_single_board_task.s(task_id, board, board_id),
                tasks_log.s(task_id, f"[{board}]: Finished.", show_result=True)
            )
            full_tasks.append(full_chain)

        chain(
            group(full_tasks),
            tasks_log.s(task_id, "All Boards Finished! Task Finish.")
        ).apply_async()
    except Exception as e:
        log_crawl_result(db, task_id, f"Error： {e}", "ERROR")
        logger.error(f"Error： {e}")
    finally:
        db.close()
