from sqlalchemy.orm import Session
from model.ptt_content import User, Post, Comment, Board


# --- User ---
# def get_user_by_id(db: Session, user_id: int):
#     return db.query(User).filter(User.id == user_id).first()
#
# def create_user(db: Session, username: str):
#     user = User(name=username)
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user


def get_or_create_user(session: Session, username: str) -> User:
    user = session.query(User).filter_by(name=username).first()
    if user is None:
        user = User(name=username)
        session.add(user)
        session.flush()
    return user


# --- Post ---
def get_or_create_post(db: Session, raw_post: dict) -> type[Post] | None | Post:
    author = get_or_create_user(db, raw_post['author']).id
    # 先查詢是否已存在
    existing = db.query(Post).filter_by(title=raw_post['title'], author_id=author, created_at=raw_post['created_at']).first()
    if existing:
        return existing  # 已存在，直接回傳

    # 嘗試新增
    post = Post(
        author_id=author,
        board_id=raw_post['board_id'],
        title=raw_post['title'],
        created_at=raw_post['created_at'],
        content=raw_post['content']
    )
    db.add(post)
    try:
        db.commit()
        db.refresh(post)
        return post
    except Exception:
        db.rollback()
        # 有可能別人同時也在新增 → 再查一次
        return db.query(Post).filter_by(title=post.title, author_id=post.author_id).first()


def create_post_with_comments(db: Session, raw_post: dict):
    post = get_or_create_post(db, raw_post)

    for row_comment in raw_post.get('comments', []):
        row_comment = dict(row_comment)
        comment_user = get_or_create_user(db, row_comment['user']).id
        comment = Comment(
            user_id=comment_user,
            content=row_comment['content'],
            created_at=row_comment['created_at'],
            post_id=post.id  # 自動關聯
        )
        post.comments.append(comment)

    db.add(post)
    db.commit()
    db.refresh(post)  # 可回傳 post.id 等資訊
    return post


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
