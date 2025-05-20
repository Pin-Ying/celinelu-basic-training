from celery import Celery
from celery.schedules import crontab
from concurrent.futures import ThreadPoolExecutor, as_completed

from db.crud import create_defult, log_crawl_result
from db.database import SessionLocal
from tasks.ptt_datacrawl import PttCrawler

celery_app = Celery("ptt", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")
celery_app.conf.beat_schedule = {
    'crawl-ptt-hourly': {
        'task': 'tasks.celery_tasks.crawl_all_boards',
        'schedule': crontab(minute=0, hour=9),
    },
}

ALL_BOARDS = {'Stock': 1, 'Baseball': 2, 'NBA': 3, 'HatePolitics': 4, 'Lifeismoney': 5}


@celery_app.task
def crawl_all_boards():
    create_defult()

    def crawl_single_board(board, board_id):
        db = SessionLocal()
        try:
            crawler = PttCrawler(db, board, board_id)
            log_crawl_result(db, f"{board}:Crawling Start!")
            posts = crawler.run()
            log_crawl_result(db, f"{board}:Finish! Crawled {len(posts)} posts")
        except Exception as e:
            log_crawl_result(db, f"{board}:Error! {e}", "ERROR")
            print(f"[{board} Error]: {e}")
        finally:
            db.close()

    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [
                executor.submit(crawl_single_board, board, board_id)
                for board, board_id in ALL_BOARDS.items()
            ]
            for future in as_completed(futures):
                future.result()
    except Exception as e:
        print(f"[Error]: {e}")


if __name__ == '__main__':
    crawl_all_boards()
