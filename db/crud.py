from sqlalchemy.orm import Session, aliased
from sqlalchemy.exc import OperationalError, SQLAlchemyError, IntegrityError
import time

from model.ptt_content import User, Post, Comment, Board, Log
from schema.ptt_content import PostInput, CommentInput, PostSearch
from db.database import Base, engine, SessionLocal


def create_default():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    all_boards = {'home-sale': 1, 'basketballTW': 2, 'NBA': 3, 'car': 4, 'Lifeismoney': 5}
    seed_boards(db, all_boards)
    db.close()


def clean_tables():
    db = SessionLocal()
    db.query(Comment).delete()
    db.query(Post).delete()
    db.query(User).delete()
    db.query(Log).delete()
    db.query(Board).delete()
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
def prepare_users_from_posts(db: Session, posts: list[PostInput]):
    all_usernames = set()
    for p in posts:
        all_usernames.add(p.author)
        for c in p.comments:
            all_usernames.add(c.user)

    existing_users = db.query(User).filter(User.name.in_(all_usernames)).all()
    user_map = {u.name: u for u in existing_users}

    missing_usernames = all_usernames - user_map.keys()
    username: str
    new_users = [User(name=username) for username in missing_usernames]

    if new_users:
        db.add_all(new_users)
        db.flush()

    for user in new_users:
        user_map[user.name] = user

    return user_map


def get_or_create_user(db: Session, username: str) -> type[User] | None | User:
    user = db.query(User).filter_by(name=username).first()
    if user:
        return user
    try:
        user = User(name=username)
        db.add(user)
        db.flush()  # 不 commit，讓外層統一 commit
        return user
    except IntegrityError:
        db.rollback()
        return db.query(User).filter_by(name=username).first()


# --- Post ---
def post_from_pydantic_to_sqlalchemy(post_input: PostInput, author_id: int) -> Post:
    return Post(
        title=post_input.title,
        content=post_input.content,
        created_at=post_input.created_at,
        board_id=post_input.board_id,
        author_id=author_id
    )


def get_newest_post(db: Session, board: int):
    return db.query(Post).filter_by(board_id=board).order_by(Post.created_at.desc()).first()


def get_post_filter_by(db: Session, page_limit=50, page_offset=None, **filters):
    query_filter = db.query(Post).filter_by(**filters).order_by(Post.created_at.desc()).limit(page_limit)
    if page_offset is None:
        return query_filter.all()
    else:
        return query_filter.offset(page_offset).all()


def get_post_by_search_dic(db: Session, post_search: PostSearch):
    query = db.query(Post)

    filters = {}
    if post_search.author:
        filters['author'] = post_search.author.name
    if post_search.board:
        filters['board'] = post_search.board.name

    if filters:
        query = query.filter_by(**filters)

    if post_search.start_datetime:
        query = query.filter(Post.created_at >= post_search.start_datetime)

    if post_search.end_datetime:
        query = query.filter(Post.created_at <= post_search.end_datetime)

    return query.all()


def get_existing_post_keys(db: Session, posts: list[PostInput]):
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

    return post_keys


def create_posts_bulk(db: Session, posts: list[PostInput], batch_size: int = 20):
    created_posts = []

    try:
        existing_keys = get_existing_post_keys(db, posts)
        user_map = prepare_users_from_posts(db, posts)

        for i in range(0, len(posts), batch_size):
            posts_batch = posts[i:i + batch_size]

            for post_input in posts_batch:
                # 取得作者
                author = user_map[post_input.author]
                if author is None:
                    user = get_or_create_user(db, post_input.author)
                    author = user
                    user_map[post_input.author] = user

                post_key = (post_input.title, author.id, post_input.created_at)
                if post_key in existing_keys:
                    continue

                new_post = post_from_pydantic_to_sqlalchemy(post_input, author.id)
                db.add(new_post)
                db.flush()  # 確保拿到 post.id

                existing_keys.add(post_key)

                # 處理留言
                create_comments(db, new_post, post_input, user_map)

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
def comment_from_pydantic_to_sqlalchemy(comment_input: CommentInput, user_id: int, post_id: int):
    return Comment(
        post_id=post_id,
        user_id=user_id,
        content=comment_input.content,
        created_at=comment_input.created_at
    )


def create_comments(db: Session, new_post, post_input, user_map):
    # 處理留言（去重）
    existing_comment_rows = db.query(
        Comment.user, Comment.content, Comment.created_at
    ).filter_by(post_id=new_post.id).all()
    seen_comments = set(existing_comment_rows)

    for c in post_input.comments:
        comment_key = (c.user, c.content, c.created_at)
        if comment_key in seen_comments:
            continue
        seen_comments.add(comment_key)

        comment_user = user_map.get(c.user)
        if comment_user is None:
            comment_user = get_or_create_user(db, c.user)
            user_map[c.user] = comment_user

        comment = comment_from_pydantic_to_sqlalchemy(c, comment_user.id, new_post.id)
        db.add(comment)


# --- Board ---
def get_all_boards(db: Session):
    boards = db.query(Board).all()
    return {b.name: b.id for b in boards}


def seed_boards(db: Session, board_dic: dict):
    for name, id_ in board_dic.items():
        exists = db.query(Board).filter_by(id=id_).first()
        if not exists:
            db.add(Board(id=id_, name=name))
    db.commit()


# --- Log ---
def log_crawl_result(db: Session, message: str, level: str = "INFO"):
    log = Log(message=message, level=level)
    db.add(log)
    db.commit()


if __name__ == "__main__":
    create_default()
