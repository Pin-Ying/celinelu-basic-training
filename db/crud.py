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
def create_posts_bulk(db: Session, posts: list[PostInput]):
    created_posts = []
    try:
        for post_input in posts:
            author = get_or_create_user(db, post_input.author)

            existing = db.query(Post).filter_by(
                title=post_input.title,
                author_id=author.id,
                created_at=post_input.created_at
            ).first()
            if existing:
                continue

            new_post = Post(
                title=post_input.title,
                content=post_input.content,
                created_at=post_input.created_at,
                board_id=post_input.board_id,
                author_id=author.id
            )
            db.add(new_post)
            db.flush()

            seen_comments = set()
            for c in post_input.comments:
                comment_key = (c.user, c.content, c.created_at)
                if comment_key in seen_comments:
                    continue
                seen_comments.add(comment_key)

                comment_user = get_or_create_user(db, c.user)

                existing_comment = db.query(Comment).filter_by(
                    post_id=new_post.id,
                    user_id=comment_user.id,
                    content=c.content,
                    created_at=c.created_at
                ).first()

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

