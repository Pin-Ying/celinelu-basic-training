from concurrent.futures import ThreadPoolExecutor, as_completed
from tasks.celery_tasks import logger
from tasks.ptt_datacrawl import PttCrawler
from db.database import SessionLocal
from db.crud import create_posts_bulk, get_all_boards


def crawl_single_board_task(board: str, board_id: int):
    db = SessionLocal()
    try:
        crawler = PttCrawler(db, board, board_id)

        logger.info(f"{board}:Crawling Start!")

        posts = crawler.crawl()
        logger.info(f"{board}:Finish! Crawled {len(posts)} posts")
        save_posts_to_db(posts)
    except Exception as e:
        logger.error(f"[{board} Crawl Error]: {e}")
    finally:
        db.close()


def crawl_all_boards():
    db = SessionLocal()
    ALL_BOARDS = get_all_boards(db)
    db.close()
    try:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for board, board_id in ALL_BOARDS.items():
                futures.append(executor.submit(crawl_single_board_task, board, board_id))

            for future in as_completed(futures):
                try:
                    future.result()  # 如果有例外，會在這裡被丟出
                except Exception as e:
                    logger.error(f"[Crawl Error]: {e}", exc_info=True)
                    continue
    except Exception as e:
        logger.error(f"[ThreadPool Error]: {e}", exc_info=True)


def save_posts_to_db(post_inputs):
    db = SessionLocal()
    try:
        create_posts_bulk(db, post_inputs)
    except Exception as e:
        logger.error(f"[DB Save Error]: {e}")
    finally:
        db.close()


if __name__ == '__main__':
    crawl_all_boards()
