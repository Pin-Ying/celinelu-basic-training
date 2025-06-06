from typing import List

from sqlalchemy.orm import Session, joinedload

from db.database import Base, engine, SessionLocal
from model.ptt_content import User, Post, Comment, Board, Log
from schema.ptt_content import PostSearch, PostSchema


def create_default():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    all_boards = {'home-sale': 1, 'basketballTW': 2, 'NBA': 3, 'car': 4, 'Lifeismoney': 5}
    seed_boards(db, all_boards)
    db.close()


# --- User ---
def get_or_create_user(db: Session, username: str) -> type[User] | None | User:
    user = db.query(User).filter_by(name=username).first()
    if user:
        return user
    try:
        user = User(name=username)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        raise e


def get_existing_user_map(db: Session):
    existing_users = db.query(User).all()
    return {u.name: u for u in existing_users}


# --- Post ---
def get_latest_post(db: Session, board: int):
    return db.query(Post).filter_by(board_id=board).order_by(Post.created_at.desc()).first()


def get_or_create_post(db: Session, post_input: Post):
    post = db.query(Post).filter_by(
        title=post_input.title,
        author_id=post_input.author_id,
        created_at=post_input.created_at
    ).first()
    if post:
        return post
    try:
        db.add(post_input)
        db.commit()
        db.refresh(post_input)
        return post_input
    except Exception as e:
        db.rollback()
        raise e


def update_post_from_id(db: Session, post_id, post_schema: PostSchema):
    target_post = db.get(Post, post_id)
    author = get_or_create_user(db, post_schema.author.name)
    board = get_or_create_board(db, post_schema.board.name)
    if target_post is None:
        return None
    target_post.title = post_schema.title
    target_post.content = post_schema.content
    target_post.created_at = post_schema.created_at
    target_post.author = author
    target_post.board = board
    try:
        db.add(target_post)
        db.commit()
        db.refresh(target_post)
        return target_post
    except Exception as e:
        db.rollback()
        raise e


def delete_post_from_id(db: Session, post_id):
    target_post = db.get(Post, post_id)
    if target_post is None:
        return None
    try:
        post_copy = Post(
            id=post_id,
            title=target_post.title,
            content=target_post.content,
            author=target_post.author,
            board=target_post.board,
            created_at=target_post.created_at)
        db.delete(target_post)
        db.commit()
        return post_copy
    except Exception as e:
        db.rollback()
        raise e


def get_query_by_post_search(db: Session, post_search: PostSearch):
    query = db.query(Post).options(
        joinedload(Post.author),
        joinedload(Post.board)
    )
    filters = []
    if post_search.author:
        query = query.join(Post.author)
        filters.append(User.name == post_search.author.name)

    if post_search.board:
        query = query.join(Post.board)
        filters.append(Board.name == post_search.board.name)

    if post_search.start_datetime:
        filters.append(Post.created_at >= post_search.start_datetime)

    if post_search.end_datetime:
        filters.append(Post.created_at <= post_search.end_datetime)

    return query.filter(*filters).order_by(Post.created_at.desc())


def get_posts_by_search(db: Session, post_search: PostSearch, posts_limit=50, posts_offset=0):
    post_query = get_query_by_post_search(db, post_search)
    if post_query:
        return post_query.offset(posts_offset).limit(posts_limit).all()
    return []


def get_post_detail_by_id(db: Session, post_id: int):
    post_input = db.query(Post).filter_by(id=post_id)
    post_input = post_input.options(joinedload(Post.comments)).first()
    return post_input


# --- Comment ---
def get_or_create_comment(db: Session, comment_input: Comment):
    comment = db.query(Comment).filter_by(
        post_id=comment_input.post_id,
        user_id=comment_input.user_id,
        content=comment_input.content,
        created_at=comment_input.created_at
    ).first()
    if comment:
        return comment
    try:
        db.add(comment_input)
        db.commit()
        db.refresh(comment_input)
        return comment_input
    except Exception as e:
        db.rollback()
        raise e


def get_existing_comments_keys_list(db: Session, post_id: int) -> List:
    comments = (
        db.query(Comment)
        .filter_by(post_id=post_id)
        .options(joinedload(Comment.user))
        .all()
    )
    if comments:
        return [(comment.user.name, comment.content, comment.created_at) for comment in comments]
    return []


def create_comments_bulk(db: Session, comments: List[Comment]):
    try:
        db.add_all(comments)
        db.commit()
        db.refresh(comments)
        return comments
    except Exception as e:
        db.rollback()
        raise e


# --- Board ---
def get_all_boards(db: Session):
    boards = db.query(Board).all()
    return {b.name: b.id for b in boards}


def get_or_create_board(db: Session, boardname: str) -> Board | type[Board]:
    board = db.query(Board).filter_by(name=boardname).first()
    if board:
        return board
    try:
        board = Board(name=boardname)
        db.add(board)
        db.commit()
        db.refresh(board)
        return board
    except Exception as e:
        db.rollback()
        raise e


def seed_boards(db: Session, board_dic: dict):
    for name, id_ in board_dic.items():
        exists = db.query(Board).filter_by(id=id_).first()
        if not exists:
            db.add(Board(id=id_, name=name))
    db.commit()


# --- Log ---
def log_crawl_result(db: Session, task_id: str, message: str, level: str = "INFO"):
    log = Log(task_id=task_id, message=message, level=level)
    db.add(log)
    db.commit()


if __name__ == "__main__":
    create_default()
