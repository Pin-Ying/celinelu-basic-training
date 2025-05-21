from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, SQLAlchemyError
import time

from model.ptt_content import User, Post, Comment, Board, Log
from schema.ptt_content import PostInput
from db.database import Base, engine, SessionLocal


def create_defult():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    seed_boards(db)
    db.close()

def clean_tables():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    db.query(Comment).delete()
    db.query(Post).delete()
    db.query(User).delete()
    db.commit()
    db.close()


def safe_commit(session: Session, retries: int = 3, delay: float = 0.5):
    for attempt in range(retries):
        try:
            session.commit()
            return
        except OperationalError as e:
            if "Deadlock found" in str(e):
                session.rollback()
                time.sleep(delay)
                continue
            raise
        except Exception:
            session.rollback()
            raise
    raise Exception("Deadlock could not be resolved after retries.")


# --- User ---
# def get_user_by_id(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()
#

def get_or_create_user(session: Session, username: str) -> User:
    user = session.query(User).filter_by(name=username).first()
    if user is None:
        user = User(name=username)
        session.add(user)
        session.flush()
    return user


# --- Post ---
def get_newest_post(db: Session):
    return db.query(Post).order_by(Post.created_at.desc()).first()


def get_existing_post_keys(db: Session, posts: list[PostInput]) -> set[tuple[str, int, datetime]]:
    min_date = min(p.created_at for p in posts)
    max_date = max(p.created_at for p in posts)

    # 預查作者資訊
    authors = list(set(p.author for p in posts))
    author_map = {
        u.name: u.id for u in db.query(User).filter(User.name.in_(authors)).all()
    }

    post_keys = set()
    if author_map:
        existing_posts = db.query(Post.title, Post.author_id, Post.created_at).filter(
            Post.created_at >= min_date,
            Post.created_at <= max_date
        ).all()

        post_keys = set((p.title, p.author_id, p.created_at) for p in existing_posts)

    return post_keys, author_map


def create_posts_bulk(db: Session, posts: list[PostInput]):
    created_posts = []
    try:
        # 預先查詢現有 post keys + 作者
        existing_keys, author_map = get_existing_post_keys(db, posts)

        for post_input in posts:
            # 取得作者（若不存在就建立）
            author_id = author_map.get(post_input.author)
            if author_id is None:
                user = get_or_create_user(db, post_input.author)
                author_id = user.id
                author_map[post_input.author] = author_id

            post_key = (post_input.title, author_id, post_input.created_at)
            if post_key in existing_keys:
                continue

            # 建立 Post
            new_post = Post(
                title=post_input.title,
                content=post_input.content,
                created_at=post_input.created_at,
                board_id=post_input.board_id,
                author_id=author_id
            )
            db.add(new_post)
            db.flush()  # 需要新 post.id 給留言用

            # 處理留言
            existing_comment = db.query(Comment.user, Comment.content, Comment.created_at).filter_by(
                post_id=new_post.id
            ).all()
            seen_comments = set((ec.user, ec.content, ec.created_at) for ec in existing_comment)
            for c in post_input.comments:
                comment_key = (c.user, c.content, c.created_at)
                if comment_key in seen_comments:
                    continue
                seen_comments.add(comment_key)

                comment_user = get_or_create_user(db, c.user)

                if existing_comment:
                    continue

                comment = Comment(
                    post_id=new_post.id,
                    user_id=comment_user.id,
                    content=c.content,
                    created_at=c.created_at
                )
                db.add(comment)

            created_posts.append(new_post)

        safe_commit(db)
    except SQLAlchemyError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise e

    return created_posts


# --- Comment ---
# def add_comment(db: Session, post_id: int, user_id: int, content: str):
#     comment = Comment(post_id=post_id, user_id=user_id, content=content)
#     db.add(comment)
#     db.commit()
#     db.refresh(comment)
#     return comment


# --- Board ---
all_boards = {'Stock': 1, 'Baseball': 2, 'NBA': 3, 'HatePolitics': 4, 'Lifeismoney': 5}


def seed_boards(db: Session):
    for name, id_ in all_boards.items():
        exists = db.query(Board).filter_by(id=id_).first()
        if not exists:
            db.add(Board(id=id_, name=name))
    db.commit()


# --- Log ---
def log_crawl_result(db: Session, message: str, level: str = "INFO"):
    log = Log(message=message, level=level)
    db.add(log)
    db.commit()
