from sqlalchemy.orm import Session
from model.ptt_content import User, Post, Comment, Board


# --- User ---
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, username: str):
    user = User(name=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_or_create_user(session: Session, username: str) -> User:
    user = session.query(User).filter_by(name=username).first()
    if user is None:
        user = User(name=username)
        session.add(user)
        session.flush()
    return user


# --- Post ---
def create_post(db: Session, title: str, content: str, author_id: int, board_id: int):
    post = Post(title=title, content=content, author_id=author_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_post(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()


def create_post_with_comments(db: Session, raw_post: dict):
    post = Post(
        author=raw_post['author'],
        title=raw_post['title'],
        created_at=raw_post['created_at'],
        content=raw_post['content']
    )

    # for c in raw_post.get('comments', []):
    #     dt = parse_comment_datetime(c['created_at'])
    #     if not dt:
    #         continue  # 跳過格式錯的留言
    #
    #     comment = Comment(
    #         user=c['user'],
    #         content=c['content'],
    #         created_at=dt,
    #         post=post  # 自動關聯
    #     )
    #     # 可選 post.comments.append(comment)
    #
    # db.add(post)
    # db.commit()
    # db.refresh(post)  # 可回傳 post.id 等資訊
    # return post


# --- Comment ---
def add_comment(db: Session, post_id: int, user_id: int, content: str):
    comment = Comment(post_id=post_id, user_id=user_id, content=content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


# --- Board ---
all_boards = {'Stock': 1, 'Baseball': 2, 'NBA': 3, 'HatePolitics': 4, 'Lifeismoney': 5}


def seed_boards(db: Session):
    for name, id_ in all_boards.items():
        exists = db.query(Board).filter_by(id=id_).first()
        if not exists:
            db.add(Board(id=id_, name=name))
    db.commit()
